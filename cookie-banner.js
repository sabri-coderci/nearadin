<!-- Çerez İzin Paneli ve JS -->
    <script>
      function checkCookieConsent() {{
        var consent = localStorage.getItem('user_cookie_consent');
        if (consent === 'granted') {{
          loadTrackingScripts();
        }} else if (!consent) {{
          document.getElementById('cookie-banner').style.display = 'block';
        }}
      }}

      function acceptCookies() {{
        localStorage.setItem('user_cookie_consent', 'granted');
        document.getElementById('cookie-banner').style.display = 'none';
        loadTrackingScripts();
      }}

      function rejectCookies() {{
        localStorage.setItem('user_cookie_consent', 'denied');
        document.getElementById('cookie-banner').style.display = 'none';
      }}

      function loadTrackingScripts() {{
        if (window.trackingScriptsLoaded) return;
        window.trackingScriptsLoaded = true;
        // Takip kodunuz
      }}

      document.addEventListener("DOMContentLoaded", checkCookieConsent);
    </script>
