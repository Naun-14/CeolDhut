/* ============================================================
   CeòlDhut — Shared HTML Components
   components.js — navbar, player bar, playlist modal
   ============================================================ */

function renderNavbar(activePage = '') {
  const user = Auth.user();
  const pages = [
    { id: 'home',    href: 'index.html',   label: 'Discover' },
    { id: 'music',   href: 'music.html',   label: 'Music' },
    { id: 'events',  href: 'events.html',  label: 'Events' },
    { id: 'artists', href: 'artists.html', label: 'Artists' },
  ];

  const links = pages.map(p =>
    `<a href="${p.href}" class="nav-link${activePage === p.id ? ' active' : ''}">${p.label}</a>`
  ).join('');

  const mobileLinks = pages.map(p =>
    `<a href="${p.href}" class="nav-link${activePage === p.id ? ' active' : ''}">${p.label}</a>`
  ).join('');

  const authRight = Auth.isLoggedIn()
    ? `<a href="account.html" class="nav-btn nav-btn-ghost" id="nav-account-btn">
         ${user && user.email ? user.email.split('@')[0] : 'Account'}
       </a>
       <button class="nav-btn nav-btn-ghost" onclick="Auth.logout()">Logout</button>`
    : `<a href="login.html" class="nav-btn nav-btn-ghost" id="nav-login-btn">Login</a>
       <a href="login.html" class="nav-btn nav-btn-fill">Join Free</a>`;

  return `
  <nav class="navbar" id="navbar">
    <div class="nav-inner">
      <a href="index.html" class="nav-logo">
        <img src="https://i.ibb.co/N6QMp4RY/logo-png.png" alt="CeòlDhut" onerror="this.style.display='none'">
        <span class="nav-logo-text">CeòlDhut</span>
      </a>
      <div class="nav-links">${links}</div>
      <div class="nav-right">${authRight}</div>
      <button class="hamburger" id="hamburger" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>
  <div class="mobile-nav" id="mobile-nav">
    ${mobileLinks}
    ${Auth.isLoggedIn()
      ? `<a href="account.html" class="nav-link">Account</a>
         <a href="#" class="nav-link" onclick="Auth.logout()">Logout</a>`
      : `<a href="login.html" class="nav-link">Login</a>`}
  </div>`;
}

function renderPlayerBar() {
  return `
  <div class="player-bar" id="player-bar" style="display:none">
    <div class="player-track">
      <div class="player-thumb" id="player-thumb">🎵</div>
      <div>
        <div class="player-track-name" id="player-track-name">Nothing playing</div>
        <div class="player-track-artist" id="player-track-artist"></div>
      </div>
      <button class="player-like" id="player-like">♡</button>
    </div>
    <div class="player-controls">
      <div class="player-btns">
        <button class="player-btn" title="Shuffle">⇄</button>
        <button class="player-btn" title="Previous">⏮</button>
        <button class="player-play" id="player-play">▶</button>
        <button class="player-btn" title="Next">⏭</button>
        <button class="player-btn" title="Repeat">↺</button>
      </div>
      <div class="player-progress">
        <span class="player-time" id="player-current">0:00</span>
        <div class="progress-track" id="progress-track">
          <div class="progress-fill" id="progress-fill"></div>
        </div>
        <span class="player-time" id="player-total">0:00</span>
      </div>
    </div>
    <div class="player-volume">
      <span class="volume-icon">🔊</span>
      <input type="range" class="volume-slider" id="volume-slider" min="0" max="100" value="80">
    </div>
  </div>`;
}

function renderPlaylistModal() {
  return `
  <div class="modal-overlay" id="playlist-modal">
    <div class="modal">
      <div class="modal-header">
        <h3 class="modal-title">Add to Playlist</h3>
        <button class="modal-close" data-modal-close>✕</button>
      </div>
      <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:16px">
        Adding: <strong id="playlist-track-name"></strong>
      </p>
      <div id="playlist-modal-list" style="margin-bottom:20px;display:flex;flex-direction:column;gap:4px"></div>
      <div style="border-top:1px solid var(--border);padding-top:16px">
        <p style="font-size:0.8rem;color:var(--text-muted);margin-bottom:10px">Create new playlist</p>
        <div style="display:flex;gap:8px">
          <input class="form-input" id="new-playlist-name" placeholder="Playlist name" style="flex:1">
          <button class="btn btn-primary btn-sm" id="create-playlist-btn">Create</button>
        </div>
      </div>
    </div>
  </div>`;
}

function injectSharedComponents(activePage) {
  // Inject navbar
  const navTarget = document.getElementById('navbar-placeholder');
  if (navTarget) navTarget.outerHTML = renderNavbar(activePage);
  else document.body.insertAdjacentHTML('afterbegin', renderNavbar(activePage));

  // Inject player
  document.body.insertAdjacentHTML('beforeend', renderPlayerBar());

  // Inject playlist modal
  document.body.insertAdjacentHTML('beforeend', renderPlaylistModal());

  // Create playlist handler
  const createPlaylistBtn = document.getElementById('create-playlist-btn');
  if (createPlaylistBtn) createPlaylistBtn.addEventListener('click', async () => {
    const nameInput = document.getElementById('new-playlist-name');
    const name = nameInput ? nameInput.value.trim() : '';
    if (!name) return;
    if (!Auth.isLoggedIn()) { Toast.error('Please login first'); return; }
    const data = await Api.post('/playlists', { name });
    if (data.id) {
      Toast.success(`Playlist "${name}" created!`);
      nameInput.value = '';
      closeModal('playlist-modal');
    } else {
      Toast.error(data.error || 'Failed to create playlist');
    }
  });
}
