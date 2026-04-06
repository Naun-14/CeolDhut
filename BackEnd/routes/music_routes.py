from flask import Blueprint, request, jsonify
import os

music_bp = Blueprint("music", __name__)


def clear_invalid_proxy_settings():
    proxy_keys = [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
        "GIT_HTTP_PROXY",
        "GIT_HTTPS_PROXY",
    ]
    for key in proxy_keys:
        value = os.getenv(key)
        if value and "127.0.0.1:9" in value:
            os.environ.pop(key, None)


def load_spotify():
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        return spotipy, SpotifyClientCredentials
    except ImportError:
        return None, None

def get_spotify_client():
    clear_invalid_proxy_settings()
    spotipy, SpotifyClientCredentials = load_spotify()
    if not spotipy or not SpotifyClientCredentials:
        return None

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return None
    
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    return spotipy.Spotify(auth_manager=auth_manager)


@music_bp.route("/search", methods=["GET"])
def search_music():
    """
    Search for music on Spotify
    
    Query params:
    - q: search query (e.g., "celtic music", "The Chieftains")
    - type: search type (track, artist, playlist) - default: track
    - limit: number of results (1-50) - default: 10
    
    Example: GET /api/music/search?q=celtic&type=track&limit=10
    """
    
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Spotify credentials not configured"}), 500
    
    # Get query parameters
    query = request.args.get('q')
    search_type = request.args.get('type', 'track')
    limit = request.args.get('limit', 10, type=int)
    
    # Validation
    if not query:
        return jsonify({"error": "Search query required (q parameter)"}), 400
    
    if limit > 10:
        limit = 10
    if limit < 1:
        limit = 1
    
    if search_type not in ['track', 'artist', 'playlist']:
        return jsonify({"error": "Type must be: track, artist, or playlist"}), 400
    
    try:
        # Search Spotify
        results = sp.search(q=query, type=search_type, limit=limit)
        
        # Format response based on type
        if search_type == 'track':
            tracks = []
            for track in results['tracks']['items']:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track.get('popularity', 0),
                    'spotify_url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] if track['album']['images'] else None
                })
            
            return jsonify({
                "type": "tracks",
                "query": query,
                "count": len(tracks),
                "results": tracks
            }), 200
        
        elif search_type == 'artist':
            artists = []
            for artist in results['artists']['items']:
                artists.append({
                    'id': artist['id'],
                    'name': artist['name'],
                    'genres': artist['genres'],
                    'popularity': artist['popularity'],
                    'followers': artist['followers']['total'],
                    'spotify_url': artist['external_urls']['spotify'],
                    'image': artist['images'][0]['url'] if artist['images'] else None
                })
            
            return jsonify({
                "type": "artists",
                "query": query,
                "count": len(artists),
                "results": artists
            }), 200
        
        elif search_type == 'playlist':
            playlists = []
            for playlist in results['playlists']['items']:
                playlists.append({
                    'id': playlist['id'],
                    'name': playlist['name'],
                    'description': playlist['description'],
                    'tracks': playlist['tracks']['total'],
                    'owner': playlist['owner']['display_name'],
                    'spotify_url': playlist['external_urls']['spotify'],
                    'image': playlist['images'][0]['url'] if playlist['images'] else None
                })
            
            return jsonify({
                "type": "playlists",
                "query": query,
                "count": len(playlists),
                "results": playlists
            }), 200
    
    except Exception as e:
        return jsonify({"error": f"Spotify search failed: {str(e)}"}), 500


@music_bp.route("/artist/<artist_id>", methods=["GET"])
def get_artist_details(artist_id):
    spotipy, _ = load_spotify()
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Spotify integration not configured"}), 500
    
    try:
        artist = sp.artist(artist_id)
        
        return jsonify({
            'id': artist['id'],
            'name': artist['name'],
            'genres': artist['genres'],
            'popularity': artist.get('popularity', 0),
            'followers': artist['followers']['total'],
            'spotify_url': artist['external_urls']['spotify'],
            'image': artist['images'][0]['url'] if artist['images'] else None,
            'external_urls': artist['external_urls']
        }), 200
    
    except spotipy.exceptions.SpotifyException as e:
        return jsonify({"error": f"Artist not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to get artist: {str(e)}"}), 500


@music_bp.route("/track/<track_id>", methods=["GET"])
def get_track_details(track_id):
    spotipy, _ = load_spotify()
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Spotify integration not configured"}), 500
    
    try:
        track = sp.track(track_id)
        
        return jsonify({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
            'album': track['album']['name'],
            'duration_ms': track['duration_ms'],
            'popularity': track.get('popularity', 0),
            'release_date': track['album']['release_date'],
            'spotify_url': track['external_urls']['spotify'],
            'image': track['album']['images'][0]['url'] if track['album']['images'] else None
        }), 200
    
    except spotipy.exceptions.SpotifyException as e:
        return jsonify({"error": f"Track not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to get track: {str(e)}"}), 500


@music_bp.route("/search/celtic", methods=["GET"])
def search_celtic_music():
    """
    Simplified endpoint specifically for Celtic music
    
    Query params:
    - limit: number of results (1-50) - default: 20
    
    Example: GET /api/music/search/celtic?limit=20
    """
    
    sp = get_spotify_client()
    if not sp:
        return jsonify({"error": "Spotify credentials not configured"}), 500
    
    limit = request.args.get('limit', 20, type=int)
    
    if limit > 10:
        limit = 10
    if limit < 1:
        limit = 1
    
    try:
        # Search for Celtic music
        results = sp.search(
            q='genre:celtic OR "Celtic Music"',
            type='track',
            limit=limit
        )
        
        tracks = []
        for track in results['tracks']['items']:
                tracks.append({
                    'id': track['id'],
                    'name': track['name'],
                    'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'popularity': track.get('popularity', 0),
                    'spotify_url': track['external_urls']['spotify'],
                    'image': track['album']['images'][0]['url'] if track['album']['images'] else None
                })
        
        return jsonify({
            "type": "Celtic Music",
            "count": len(tracks),
            "results": tracks
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Celtic music search failed: {str(e)}"}), 500
