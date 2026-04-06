/* ============================================================
   CeòlDhut — Shared Utilities
   api.js — API layer, auth helpers, toast, player
   ============================================================ */

const API_BASE = (() => {
  const origin = window.location.origin;
  if (origin.startsWith('http://') || origin.startsWith('https://')) {
    return '/api';
  }
  return 'http://127.0.0.1:5000/api';
})();

/* ── Auth ──────────────────────────────────────────────── */
const Auth = {
  save(token, user) {
    localStorage.setItem('ceol_token', token);
    localStorage.setItem('ceol_user', JSON.stringify(user));
  },
  token() { return localStorage.getItem('ceol_token'); },
  user() {
    try { return JSON.parse(localStorage.getItem('ceol_user')); }
    catch { return null; }
  },
  isLoggedIn() { return !!this.token(); },
  isAdmin() { return this.user()?.role === 'ADMIN'; },
  logout() {
    localStorage.removeItem('ceol_token');
    localStorage.removeItem('ceol_user');
    window.location.href = 'login.html';
  },
  headers() {
    const h = { 'Content-Type': 'application/json' };
    if (this.token()) h['Authorization'] = `Bearer ${this.token()}`;
    return h;
  }
};

/* ── API ───────────────────────────────────────────────── */
const Api = {
  async get(path) {
    const res = await fetch(API_BASE + path, { headers: Auth.headers() });
    return res.json();
  },
  async post(path, body) {
    const res = await fetch(API_BASE + path, {
      method: 'POST',
      headers: Auth.headers(),
      body: JSON.stringify(body)
    });
    return res.json();
  },
  async put(path, body) {
    const res = await fetch(API_BASE + path, {
      method: 'PUT',
      headers: Auth.headers(),
      body: JSON.stringify(body)
    });
    return res.json();
  },
  async del(path) {
    const res = await fetch(API_BASE + path, {
      method: 'DELETE',
      headers: Auth.headers()
    });
    return res.json();
  }
};

/* ── Toast ─────────────────────────────────────────────── */
const Toast = {
  container: null,
  init() {
    this.container = document.getElementById('toast-container');
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    }
  },
  show(msg, type = 'success', duration = 3000) {
    if (!this.container) this.init();
    const icons = { success: '✓', error: '✕', info: 'ℹ' };
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<span>${icons[type] || icons.info}</span><span>${msg}</span>`;
    this.container.appendChild(t);
    setTimeout(() => {
      t.style.animation = 'slideInRight 0.3s ease reverse';
      setTimeout(() => t.remove(), 280);
    }, duration);
  },
  success(msg) { this.show(msg, 'success'); },
  error(msg) { this.show(msg, 'error'); },
  info(msg) { this.show(msg, 'info'); }
};

/* ── Player ────────────────────────────────────────────── */
const Player = {
  current: null,
  isPlaying: false,
  progress: 0,
  interval: null,

  init() {
    this.bar = document.getElementById('player-bar');
    this.playBtn = document.getElementById('player-play');
    this.trackName = document.getElementById('player-track-name');
    this.trackArtist = document.getElementById('player-track-artist');
    this.trackThumb = document.getElementById('player-thumb');
    this.progressFill = document.getElementById('progress-fill');
    this.currentTime = document.getElementById('player-current');
    this.totalTime = document.getElementById('player-total');
    this.volumeSlider = document.getElementById('volume-slider');
    if (this.playBtn) this.playBtn.addEventListener('click', () => this.togglePlay());
    if (this.volumeSlider) this.volumeSlider.addEventListener('input', e => this.setVolume(e.target.value));
    const progressTrack = document.getElementById('progress-track');
    if (progressTrack) progressTrack.addEventListener('click', e => this.seek(e));
  },

  play(track) {
    this.current = track;
    this.isPlaying = true;
    this.progress = 0;
    if (this.bar) this.bar.style.display = 'flex';
    if (this.trackName) this.trackName.textContent = track.name || track.title || 'Unknown';
    if (this.trackArtist) this.trackArtist.textContent = track.artist || '';
    if (this.trackThumb) {
      if (track.image) {
        this.trackThumb.innerHTML = `<img src="${track.image}" style="width:100%;height:100%;object-fit:cover;border-radius:8px">`;
      } else {
        this.trackThumb.innerHTML = '🎵';
      }
    }
    if (this.playBtn) this.playBtn.innerHTML = '⏸';
    if (this.totalTime) this.totalTime.textContent = this.formatMs(track.duration_ms || 180000);
    this.startProgress(track.duration_ms || 180000);
    // Open Spotify if we have a URL
    if (track.spotify_url) {
      Toast.info(`Opening in Spotify: ${track.name || track.title}`);
      setTimeout(() => window.open(track.spotify_url, '_blank'), 600);
    }
  },

  togglePlay() {
    if (!this.current) return;
    this.isPlaying = !this.isPlaying;
    if (this.playBtn) this.playBtn.innerHTML = this.isPlaying ? '⏸' : '▶';
    if (this.isPlaying) {
      this.startProgress(this.current.duration_ms || 180000);
    } else {
      clearInterval(this.interval);
    }
  },

  startProgress(totalMs) {
    clearInterval(this.interval);
    const total = totalMs / 1000;
    this.interval = setInterval(() => {
      if (!this.isPlaying) return;
      this.progress += 0.5;
      if (this.progress >= total) { this.progress = 0; this.isPlaying = false; if (this.playBtn) this.playBtn.innerHTML = '▶'; clearInterval(this.interval); }
      const pct = (this.progress / total) * 100;
      if (this.progressFill) this.progressFill.style.width = pct + '%';
      if (this.currentTime) this.currentTime.textContent = this.formatSec(this.progress);
    }, 500);
  },

  seek(e) {
    if (!this.current) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    const total = (this.current.duration_ms || 180000) / 1000;
    this.progress = pct * total;
    if (this.progressFill) this.progressFill.style.width = (pct * 100) + '%';
    if (this.currentTime) this.currentTime.textContent = this.formatSec(this.progress);
  },

  setVolume(v) { /* audio element volume if used */ },

  formatMs(ms) { return this.formatSec(ms / 1000); },
  formatSec(s) {
    const m = Math.floor(s / 60);
    const sec = Math.floor(s % 60);
    return `${m}:${sec.toString().padStart(2, '0')}`;
  }
};

/* ── Nav helpers ───────────────────────────────────────── */
function initNav() {
  // Sticky
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    });
  }

  // Hamburger / mobile menu
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobile-nav');
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      hamburger.classList.toggle('open');
      mobileNav.classList.toggle('open');
    });
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        mobileNav.classList.remove('open');
      });
    });
  }

  // Auth-aware nav
  const loginBtn = document.getElementById('nav-login-btn');
  const accountBtn = document.getElementById('nav-account-btn');
  if (Auth.isLoggedIn()) {
    if (loginBtn) loginBtn.style.display = 'none';
    if (accountBtn) { accountBtn.style.display = 'flex'; accountBtn.textContent = Auth.user()?.email?.split('@')[0] || 'Account'; }
  } else {
    if (accountBtn) accountBtn.style.display = 'none';
  }
}

/* ── Modal helpers ─────────────────────────────────────── */
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}
function initModals() {
  document.querySelectorAll('[data-modal-close]').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.closest('.modal-overlay')?.classList.remove('open');
    });
  });
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', e => {
      if (e.target === overlay) overlay.classList.remove('open');
    });
  });
}

/* ── Playlist modal ────────────────────────────────────── */
async function openAddToPlaylist(track) {
  if (!Auth.isLoggedIn()) {
    Toast.error('Please login to add to playlist');
    setTimeout(() => window.location.href = 'login.html', 1000);
    return;
  }
  // Fetch playlists
  const data = await Api.get('/playlists');
  const playlists = data.playlists || [];
  const listEl = document.getElementById('playlist-modal-list');
  if (!listEl) return;
  listEl.innerHTML = '';
  if (playlists.length === 0) {
    listEl.innerHTML = '<p style="color:var(--text-muted);font-size:0.875rem">No playlists yet. Create one below.</p>';
  } else {
    playlists.forEach(pl => {
      const item = document.createElement('div');
      item.className = 'playlist-item';
      item.style.cursor = 'pointer';
      item.innerHTML = `<div class="playlist-thumb">🎵</div><span class="playlist-name">${pl.name}</span>`;
      item.addEventListener('click', async () => {
        // First ensure track exists in DB
        const tRes = await Api.post('/tracks', {
          title: track.name || track.title,
          spotify_id: track.id || track.spotify_id,
          duration_ms: track.duration_ms
        });
        const trackId = tRes.id;
        if (!trackId) { Toast.error('Could not save track'); return; }
        const r = await Api.post(`/tracks/playlist/${pl.id}/tracks`, { track_id: trackId });
        if (r.message) { Toast.success(`Added to "${pl.name}"`); closeModal('playlist-modal'); }
        else Toast.error(r.error || 'Failed to add track');
      });
      listEl.appendChild(item);
    });
  }
  document.getElementById('playlist-track-name').textContent = track.name || track.title || '';
  openModal('playlist-modal');
}

document.addEventListener('DOMContentLoaded', () => {
  Toast.init();
  initNav();
  initModals();
  Player.init();
});
