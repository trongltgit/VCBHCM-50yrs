# app.py (Phiên bản Cuối cùng & Tối ưu hóa Toàn diện Desktop/Mobile)
from flask import Flask, redirect, url_for, Response

app = Flask(__name__)

# =========================================================================
# --- HTML TRANG CHÍNH (MAIN PAGE - ALBUM/TABS) ---
# (ĐÃ TỐI ƯU HÓA KÍCH THƯỚC HEADER CHO DESKTOP)
# =========================================================================

MAIN_PAGE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kỷ niệm 50 năm Vietcombank Chi nhánh TP. Hồ Chí Minh</title>
    <style>
        /* CSS TỔNG QUAN */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        /* HEADER VÀ TIÊU ĐỀ */
        .main-header {
            background-color: white;
            padding: 10px 0; 
            border-bottom: 3px solid #007044;
            text-align: center;
        }

        .main-header .logo {
            max-width: 200px; 
            height: auto;
            margin-bottom: 5px; 
        }

        .main-header h1 {
            color: #007044;
            font-size: 1.2em; 
            margin: 0;
            padding: 0 10px; 
        }
        
        /* MEDIA QUERY cho Desktop (Tối ưu hóa Header Gọn gàng) */
        @media (min-width: 768px) {
             .main-header {
                padding: 15px 0; /* Giảm padding tổng thể */
            }
            .main-header .logo {
                max-width: 250px; /* Giảm kích thước logo Desktop */
                margin-bottom: 8px;
            }
            .main-header h1 {
                font-size: 1.6em; /* Giảm font size Desktop */
                padding: 0 20px;
            }
        }

        /* THANH ĐIỀU HƯỚNG (TABS) - Tối ưu CUỘN NGANG */
        .nav-tabs {
            display: flex;
            justify-content: flex-start; 
            background-color: #007044;
            padding: 0;
            margin: 0;
            overflow-x: auto; 
            -webkit-overflow-scrolling: touch; 
            white-space: nowrap; 
        }

        .nav-tabs::-webkit-scrollbar {
             display: none; /* Ẩn scrollbar trên Chrome/Safari/Opera */
        }

        .nav-tabs .tab {
            padding: 15px 15px; 
            color: white;
            text-decoration: none;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.3s, color 0.3s;
            border-bottom: 3px solid transparent;
            flex-shrink: 0; 
            font-size: 0.9em;
        }

        .nav-tabs .tab:hover {
            background-color: #005030;
        }

        .nav-tabs .tab.active {
            background-color: #f4f4f4;
            color: #007044;
            border-bottom: 3px solid #f4f4f4;
        }
        
        /* VÙNG NỘI DUNG CHÍNH */
        .content-area {
            padding: 15px; 
            min-height: 70vh;
            background-color: white;
            margin: 10px auto; 
            max-width: 1200px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            border-radius: 4px;
        }

        .tab-content {
            display: none;
            padding: 10px 0;
        }
        
        .tab-content.active {
            display: block;
        }
        
        /* Nội dung Giới Thiệu & Lịch sử (PDF Embed) */
        .pdf-viewer {
            width: 100%;
            height: 60vh; 
            border: 1px solid #ccc;
            min-height: 500px; 
        }

        .introduction-text {
            line-height: 1.5; 
            margin-bottom: 15px;
            text-align: justify; 
        }
        
        /* --- Nội dung Album Ảnh (Image Grid) --- */
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 10px; 
        }

        .image-item {
            overflow: hidden;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
            cursor: pointer; 
        }

        .image-item img {
            width: 100%;
            height: 150px; 
            object-fit: cover;
            display: block;
            transition: transform 0.5s;
        }
        
        .image-item:hover img {
            transform: scale(1.05);
        }

        .image-caption {
            padding: 8px; 
            background-color: #007044;
            color: white;
            text-align: center;
            font-size: 0.8em; 
        }
        
        /* --- Modal (Phóng to ảnh) --- */
        #image-modal {
            display: none; 
            position: fixed;
            z-index: 2000; 
            padding-top: 50px; 
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto; 
            background-color: rgba(0,0,0,0.9); 
        }

        #modal-content {
            margin: auto;
            display: block;
            width: 90%;
            max-width: 900px;
            max-height: 90vh; 
            object-fit: contain; 
        }

        #modal-caption {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
            text-align: center;
            color: #ccc;
            padding: 10px 0;
        }

        #close-modal {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        }

        #close-modal:hover,
        #close-modal:focus {
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }

        /* Nội dung Audio/Video */
        .media-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .media-container video, .media-container audio {
            width: 100%;
            margin-bottom: 15px;
        }
        
        .audio-controls {
            display: flex;
            align-items: center;
            background: #007044;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            width: 100%;
            justify-content: space-between;
        }

        #app-toggle-audio-btn {
            background: transparent;
            color: white;
            border: none;
            padding: 0;
            font-size: 18px;
            cursor: pointer;
            margin-right: 15px;
        }
        
        .time-display {
            font-family: monospace;
            font-size: 0.9em;
        }
        
        /* Media Query cho Tablet/Desktop */
        @media (min-width: 768px) {
            .content-area {
                margin: 20px auto;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            .pdf-viewer {
                height: 80vh; 
                min-height: 700px;
            }
            .image-grid {
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
            }
            .image-item img {
                height: 200px;
            }
            .image-caption {
                padding: 10px;
                font-size: 0.9em;
            }
            .nav-tabs .tab {
                padding: 15px 25px;
                font-size: 1em;
            }
        }
    </style>
</head>
<body>
    
    <audio id="background-music" src="static/HANH KHUC VCB_CUT.mp3" preload="metadata"></audio>

    <header class="main-header">
        <img src="static/Logo-50-yrs.png" alt="Logo Kỷ niệm 50 năm" class="logo">
        <h1>Kỷ niệm 50 năm thành lập Vietcombank Chi nhánh TP. Hồ Chí Minh</h1>
    </header>

    <nav class="nav-tabs">
        <a class="tab active" data-tab="gioi-thieu">Giới thiệu</a>
        <a class="tab" data-tab="album-anh">Album ảnh</a>
        <a class="tab" data-tab="video">Video</a>
        <a class="tab" data-tab="nhac">Nhạc</a>
        <a class="tab" data-tab="lich-su">Lịch sử phát triển</a>
    </nav>

    <main class="content-area">
        
        <div id="gioi-thieu" class="tab-content active">
            <h2 style="color:#007044;">Lời giới thiệu</h2>
            
            <p class="introduction-text">
                Chào mừng quý vị đến với không gian kỷ niệm 50 năm thành lập Vietcombank Chi nhánh TP. Hồ Chí Minh. Đây là cột mốc quan trọng đánh dấu nửa thế kỷ hình thành và phát triển, gắn bó cùng sự phồn vinh của thành phố.
                Chúng tôi trân trọng gửi lời cảm ơn sâu sắc đến toàn thể cán bộ nhân viên, khách hàng và đối tác đã đồng hành trong suốt chặng đường qua.
            </p>
            <p>
                Để xem tài liệu giới thiệu đầy đủ, vui lòng tải hoặc xem trực tiếp bên dưới: 
                <a href="static/introduction.pdf" target="_blank" style="color: #007044; font-weight: bold;">[Tải file Giới thiệu (PDF)]</a>
            </p>
            
            <iframe src="static/introduction.pdf" class="pdf-viewer">
                Trình duyệt của bạn không hỗ trợ hiển thị PDF nhúng.
            </iframe>
        </div>

        <div id="album-anh" class="tab-content">
            <h2 style="color:#007044;">Album Ảnh Kỷ Niệm 50 Năm</h2>
            <div class="image-grid">
                
                <div class="image-item" data-src="static/photo_1.jpg" data-caption="Hoạt động sự kiện Chi nhánh VCB TP.HCM">
                    <img src="static/photo_1.jpg" alt="Hoạt động sự kiện">
                    <div class="image-caption">Hoạt động sự kiện Chi nhánh VCB TP.HCM</div>
                </div>
                
                <div class="image-item" data-src="static/photo_2.jpg" data-caption="Lễ vinh danh và tri ân">
                    <img src="static/photo_2.jpg" alt="Vinh danh cán bộ">
                    <div class="image-caption">Lễ vinh danh và tri ân</div>
                </div>
                
                <div class="image-item" data-src="static/photo_3.jpg" data-caption="Hình ảnh tập thể chi nhánh">
                    <img src="static/photo_3.jpg" alt="Tập thể">
                    <div class="image-caption">Hình ảnh tập thể chi nhánh</div>
                </div>
                
                </div>
        </div>
        
        <div id="video" class="tab-content">
            <h2 style="color:#007044;">Video Kỷ Niệm</h2>
            <div class="media-container">
                <video id="main-video" controls width="100%" height="auto" poster="static/video_poster.jpg" playsinline>
                    <source src="static/VCB60yrs.mp4" type="video/mp4">
                    Trình duyệt của bạn không hỗ trợ thẻ video.
                </video>
            </div>
        </div>
        
        <div id="nhac" class="tab-content">
            <h2 style="color:#007044;">Nhạc Kỷ Niệm (Hành Khúc VCB)</h2>
            <div class="media-container">
                
                <div class="audio-controls">
                    <button id="app-toggle-audio-btn">🔇</button>
                    <div class="time-display" id="app-audio-time-display">0:00 / 0:00</div>
                </div>
                
                <h3 style="color:#007044;">Lời bài hát:</h3>
                <p>Xem file PDF lời bài hát: <a href="static/HANHKHUCVCB.pdf" target="_blank" style="color: #007044; font-weight: bold;">[Mở PDF Lời Bài Hát]</a></p>
                
                <iframe id="music-lyrics-pdf" src="static/HANHKHUCVCB.pdf" class="pdf-viewer">
                    Trình duyệt của bạn không hỗ trợ hiển thị PDF nhúng.
                </iframe>
            </div>
        </div>

        <div id="lich-su" class="tab-content">
            <h2 style="color:#007044;">Lịch Sử Phát Triển</h2>
            <iframe id="lichsu-pdf-viewer" src="static/lichsuphattrien.pdf" class="pdf-viewer">
                Trình duyệt của bạn không hỗ trợ hiển thị PDF nhúng.
            </iframe>
        </div>

    </main>
    
    <div id="image-modal">
        <span id="close-modal">&times;</span>
        <img id="modal-content">
        <div id="modal-caption"></div>
    </div>
    
    <script>
        const music = document.getElementById('background-music');
        const tabs = document.querySelectorAll('.nav-tabs .tab');
        const contents = document.querySelectorAll('.tab-content');
        const toggleAudioBtn = document.getElementById('app-toggle-audio-btn');
        const audioTimeDisplay = document.getElementById('app-audio-time-display');
        const mainVideo = document.getElementById('main-video');
        const lichSuPdfViewer = document.getElementById('lichsu-pdf-viewer'); 
        
        // Modal elements
        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-content');
        const modalCaption = document.getElementById('modal-caption');
        const closeModal = document.getElementById('close-modal');
        
        let totalDuration = '0:00';
        let isMusicPlaying = false;

        // --- 1. LOGIC CHUYỂN TAB (SPA) & FIX LỖI VIDEO/PDF ---
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                const targetTab = this.getAttribute('data-tab');

                // --- Cuộn thanh tab đang active vào giữa màn hình ---
                const navTabsContainer = this.closest('.nav-tabs');
                const tabRect = this.getBoundingClientRect();
                const containerRect = navTabsContainer.getBoundingClientRect();
                
                const scrollPosition = navTabsContainer.scrollLeft + (tabRect.left + tabRect.width / 2) - (containerRect.width / 2);
                
                navTabsContainer.scrollTo({
                    left: scrollPosition,
                    behavior: 'smooth'
                });
                // -----------------------------------------------------------


                // Dừng tất cả media khi chuyển tab
                stopAllMedia();

                // Loại bỏ class active khỏi tất cả tabs và nội dung
                tabs.forEach(t => t.classList.remove('active'));
                contents.forEach(c => c.classList.remove('active'));

                // Thêm class active cho tab hiện tại và nội dung tương ứng
                this.classList.add('active');
                document.getElementById(targetTab).classList.add('active');
                
                // Xử lý logic đặc biệt cho từng tab
                if (targetTab === 'nhac') {
                    playMusic();
                } else if (targetTab === 'video') {
                    mainVideo.load(); 
                    mainVideo.play().catch(e => console.log("Không thể tự động phát video:", e)); 
                } else if (targetTab === 'lich-su') {
                    // Buộc trình duyệt tải lại nội dung iframe
                    const currentSrc = lichSuPdfViewer.src;
                    lichSuPdfViewer.src = 'about:blank'; 
                    setTimeout(() => { lichSuPdfViewer.src = currentSrc; }, 10);
                }
                
                updateTimeDisplay();
            });
        });

        // --- 2. LOGIC DỪNG/PHÁT MEDIA ---
        function stopAllMedia() {
            music.pause();
            music.currentTime = 0;
            isMusicPlaying = false;
            if (toggleAudioBtn) toggleAudioBtn.textContent = '🔇';
            
            mainVideo.pause();
            mainVideo.currentTime = 0;
            mainVideo.load(); 
        }
        
        // Hàm này được gọi từ Intro và Tab Nhạc
        function playMusic() {
            music.volume = 0.6;
            music.play().then(() => {
                isMusicPlaying = true;
                if (toggleAudioBtn) {
                       toggleAudioBtn.textContent = '🔊';
                }
            }).catch(e => {
                isMusicPlaying = false;
                if (toggleAudioBtn) {
                    toggleAudioBtn.textContent = '🔇';
                }
                console.log("Không thể tự động phát nhạc:", e);
            });
        }
        
        function toggleAudio() {
            if (music.paused) {
                if (music.currentTime >= music.duration) {
                    music.currentTime = 0;
                }
                playMusic();
            } else {
                music.pause();
                isMusicPlaying = false;
                toggleAudioBtn.textContent = '🔇';
            }
        }
        
        if (toggleAudioBtn) {
               toggleAudioBtn.addEventListener('click', toggleAudio);
        }


        // --- 3. LOGIC MODAL (PHÓNG TO ẢNH) ---
        const imageItems = document.querySelectorAll('.image-item');
        
        imageItems.forEach(item => {
            item.addEventListener('click', function() {
                modal.style.display = "block";
                modalImg.src = this.getAttribute('data-src');
                modalCaption.innerHTML = this.getAttribute('data-caption');
            });
        });

        // Đóng Modal khi click vào dấu 'x'
        closeModal.onclick = function() { 
            modal.style.display = "none";
        }
        
        // Đóng Modal khi click bên ngoài ảnh
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }

        // --- 4. LOGIC HIỂN THỊ THỜI GIAN NHẠC ---
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
        }
        
        function updateTimeDisplay() {
            if (music.readyState >= 1 && audioTimeDisplay) {
                const currentTime = music.currentTime;
                const formattedCurrent = formatTime(currentTime);
                audioTimeDisplay.textContent = `${formattedCurrent} / ${totalDuration}`;
            }
        }
        
        music.addEventListener('loadedmetadata', function() {
            if (isFinite(music.duration)) {
                totalDuration = formatTime(music.duration);
            }
            updateTimeDisplay();
        });

        music.addEventListener('timeupdate', updateTimeDisplay);


        // --- 5. Tự động kích hoạt tab Giới thiệu khi tải trang ---
        document.addEventListener('DOMContentLoaded', function() {
            // Không cần xử lý gì thêm, tab "gioi-thieu" đã active sẵn trong HTML
        });
        
    </script>
</body>
</html>
"""

# =========================================================================
# --- HTML TRANG GIỚI THIỆU (INTRO PAGE) ---
# (ĐÃ SỬA LỖI CHUYỂN HƯỚNG)
# =========================================================================

INTRO_PAGE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kỷ niệm 50 năm Vietcombank CN TPHCM - Giới thiệu</title>
    <style>
        /* --------------------------
        * CSS TỔNG QUAN
        * -------------------------- */
        body {
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            background-color: #38761d; 
            color: white;
            font-family: Arial, sans-serif;
            position: relative;
        }

        /* --------------------------
        * Lớp phủ Khởi động
        * -------------------------- */
        #intro-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000; 
            opacity: 1;
            transition: opacity 1s ease-out;
            text-align: center;
        }
        
        #brand-logo {
            max-width: 80%; 
            height: auto;
            margin-bottom: 30px; 
        }

        #cta-button {
            padding: 12px 20px; 
            font-size: 1em; 
            font-weight: bold;
            color: white;
            background-color: #007044; 
            border: 2px solid white;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s;
            margin-top: 20px;
            z-index: 1001;
            white-space: normal; 
            max-width: 90%;
        }

        #cta-button:hover {
            background-color: #005030;
            transform: scale(1.05);
        }
        
        /* Media Query cho Desktop */
        @media (min-width: 768px) {
            #brand-logo {
                max-width: 350px; 
                margin-bottom: 40px;
            }
            #cta-button {
                padding: 15px 30px;
                font-size: 1.2em;
                white-space: nowrap;
            }
        }

        /* Vùng điều khiển Audio (Bao gồm nút và thời gian) */
        .audio-controls {
            position: absolute;
            top: 10px; 
            right: 10px; 
            display: none; 
            align-items: center;
            color: white;
            font-size: 0.9em;
            z-index: 1001; 
            background: rgba(0, 0, 0, 0.5); 
            padding: 5px 8px;
            border-radius: 5px;
        }

        #toggle-audio-btn {
            background: transparent;
            color: white;
            border: none;
            padding: 0;
            font-size: 16px; 
            cursor: pointer;
            border-radius: 5px;
            margin-right: 10px;
        }
        
        #audio-time-display {
            font-family: monospace;
            font-size: 0.8em; 
        }
        
        /* ẨN HEADER VÀ DISCOVERY TAB KHI LỚP PHỦ INTRO ĐANG HIỂN THỊ */
        .header, .discovery-tab {
            display: none; 
        }

        /* Header và Logo (NỀN TRẮNG) - Sau khi Intro hoàn tất */
        .header {
            text-align: center;
            padding: 15px 0 10px 0; 
            background-color: white;
            border-bottom: 1px solid #ccc;
            width: 100%;
            position: absolute; 
            top: 0;
            left: 0;
            z-index: 20;
        }

        .logo {
            max-width: 70%; 
            height: auto;
            display: block;
            margin: 0 auto;
        }
        
        /* Media Query cho Desktop Header (Sau Intro) */
        @media (min-width: 768px) {
            .header {
                padding: 10px 0 5px 0; /* Header nhỏ hơn sau Intro */
            }
            .logo {
                max-width: 200px; /* Giảm kích thước logo Desktop sau Intro */
            }
        }


        /* Tab "Khám phá" */
        .discovery-tab {
            position: absolute;
            top: 55%; 
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 15px 25px; 
            background-color: rgba(0, 0, 0, 0.7);
            border: 2px solid #ccc;
            border-radius: 10px;
            cursor: pointer;
            text-align: center;
            font-size: 1.2em; 
            font-weight: bold;
            transition: background-color 0.3s, transform 0.3s;
            user-select: none;
            white-space: normal; 
            max-width: 80%;
            z-index: 50;
        }

        .discovery-tab:hover {
            background-color: rgba(0, 0, 0, 0.9);
            transform: translate(-50%, -50%) scale(1.03);
        }

        /* Hiệu ứng Sao băng (Stars) */
        #star-container {
            position: absolute;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }
            
        .star {
            position: absolute;
            background-color: #cccccc; 
            border-radius: 50%;
            opacity: 0;
            animation: meteor-shower linear infinite;
            pointer-events: none;
        }

        @keyframes meteor-shower {
            0% {
                transform: translate(0, 0) rotate(25deg);
                opacity: 0.8;
            }
            100% {
                transform: translate(400px, 1200px) rotate(25deg); 
                opacity: 0;
            }
        }
    </style>
</head>
<body>

    <div id="star-container"></div>

    <div id="intro-container">
        <img src="static/Logo-50-yrs.png" alt="Logo Vietcombank" id="brand-logo">
        
        <button id="cta-button">
            Bắt đầu Khám phá Kỷ niệm 50 năm
        </button>
    </div>

    <div class="audio-controls" id="audio-controls"> 
        <button id="toggle-audio-btn">🔇</button>
        <div id="audio-time-display">0:00 / 0:00</div>
    </div>

    <audio id="background-music" src="static/HANH KHUC VCB_CUT.mp3" preload="metadata"></audio>

    <div class="header" id="main-header">
        <img src="static/Logo-50-yrs.png" alt="Logo Công ty" class="logo">
    </div>

    <div class="discovery-tab" id="discovery-tab">
        Khám phá kỷ niệm 50 năm thành lập Vietcombank Chi nhánh TP. Hồ Chí Minh
    </div>


    <script>
        /* --------------------------
        * JavaScript
        * -------------------------- */
        const REDIRECT_URL = "/main"; 
        const MAX_STARS = 100; 
        const music = document.getElementById('background-music');
        const discoveryTab = document.getElementById('discovery-tab');
        const introContainer = document.getElementById('intro-container');
        const ctaButton = document.getElementById('cta-button');
        const toggleAudioBtn = document.getElementById('toggle-audio-btn');
        const starContainer = document.getElementById('star-container'); 
        const audioTimeDisplay = document.getElementById('audio-time-display');
        const mainHeader = document.getElementById('main-header');
        const audioControls = document.getElementById('audio-controls');

        let isRedirecting = false; 
        let isPlaying = false; 
        let totalDuration = '0:00';

        // Hàm format thời gian từ giây sang phút:giây
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
        }
        
        // Cập nhật hiển thị thời gian
        function updateTimeDisplay() {
            if (music.readyState >= 1) { 
                const currentTime = music.currentTime;
                const formattedCurrent = formatTime(currentTime);
                audioTimeDisplay.textContent = `${formattedCurrent} / ${totalDuration}`;
            }
        }
        
        // Hàm Bật/Tắt nhạc
        function toggleAudio() {
            if (music.paused) {
                music.volume = 0.5;
                music.play().then(() => {
                    toggleAudioBtn.textContent = '🔊';
                    isPlaying = true;
                }).catch(e => console.error("Lỗi phát nhạc:", e));
            } else {
                music.pause();
                toggleAudioBtn.textContent = '🔇';
                isPlaying = false;
            }
        }
        
        // --- LOGIC AUDIO ---
        
        music.addEventListener('loadedmetadata', function() {
            if (isFinite(music.duration)) {
                totalDuration = formatTime(music.duration);
            }
            updateTimeDisplay();
        });

        music.addEventListener('timeupdate', updateTimeDisplay);

        // --- LOGIC ĐIỀU HƯỚNG VÀ KHỞI ĐỘNG ---

        // Hàm điều hướng chính
        function handleRedirect() {
            if (isRedirecting) return;
            isRedirecting = true;
            
            console.log("Điều hướng tới /main.");
            music.pause();
            music.currentTime = 0;
            
            // Đảm bảo hiệu ứng fade out lớp phủ đen
            introContainer.style.opacity = '0';
            
            setTimeout(() => {
                    window.location.href = REDIRECT_URL;
            }, 500); // Chuyển trang sau 0.5s để hiệu ứng mờ kịp thời
        }
        
        // Hàm hiển thị nội dung chính (sau khi Intro hoàn tất)
        function showMainContent() {
             mainHeader.style.display = 'block';
             discoveryTab.style.display = 'block';
             audioControls.style.display = 'flex'; // Hiển thị bộ điều khiển nhạc
        }
        
        // FIX: TỰ ĐỘNG PHÁT NHẠC (CỐ GẮNG) KHI TẢI TRANG
        window.addEventListener('load', function() {
            // 1. Cố gắng phát nhạc ngay khi tải trang (trước khi tương tác)
            music.volume = 0.5;
            music.play().then(() => {
                toggleAudioBtn.textContent = '🔊';
                isPlaying = true;
                console.log("Nhạc tự động phát thành công.");
            }).catch(e => {
                console.log("Không thể tự động phát nhạc trước tương tác. Chờ CTA.");
                toggleAudioBtn.textContent = '🔇';
                isPlaying = false;
            });
        
            // 2. Khởi tạo hiệu ứng sao băng và ẩn nội dung chính
            for (let i = 0; i < MAX_STARS; i++) {
                createStar();
            }
            
            mainHeader.style.display = 'none';
            discoveryTab.style.display = 'none';
            audioControls.style.display = 'none';
        });

        // Logic Khởi động (CTA Button)
        ctaButton.addEventListener('click', function() {
            // 1. Đảm bảo nhạc phát (Nếu bị chặn trước đó, sẽ phát ở đây)
            if (music.paused) {
                toggleAudio();
            }

            // 2. Tắt lớp phủ (Fade out)
            introContainer.style.opacity = '0';
            setTimeout(() => {
                introContainer.style.display = 'none';
                // 3. Hiển thị nội dung chính
                showMainContent();
            }, 1000); 
        });
        
        // Đính kèm sự kiện cho nút Bật/Tắt (trên cùng bên phải)
        toggleAudioBtn.addEventListener('click', toggleAudio);


        // *** ĐIỂM QUAN TRỌNG: TỰ ĐỘNG CHUYỂN HƯỚNG KHI NHẠC KẾT THÚC ***
        music.addEventListener('ended', handleRedirect);


        // ** FIX LỖI: Click vào Tab "Khám phá" (Discovery Tab) sẽ chuyển hướng luôn
        discoveryTab.addEventListener('click', function(event) {
            event.preventDefault(); 
            // Dừng nhạc và điều hướng ngay lập tức
            music.pause(); 
            handleRedirect(); 
        });


        // --- Hiệu ứng Sao băng (Stars) ---
        function createStar() {
            const star = document.createElement('div');
            star.className = 'star';

            star.style.left = `${Math.random() * 100}vw`;
            star.style.top = `${Math.random() * -20}vh`;

            const size = Math.random() * 5 + 2; 
            star.style.width = `${size}px`;
            star.style.height = `${size}px`;

            const duration = Math.random() * 3 + 5; 
            star.style.animationDuration = `${duration}s`;
            star.style.animationDelay = `-${Math.random() * duration}s`;

            starContainer.appendChild(star);
        }
        
        // Listener để tái tạo sao băng khi animation kết thúc
        starContainer.addEventListener('animationiteration', function(e) {
             if (e.target.classList.contains('star')) {
                 // Đặt lại vị trí ngẫu nhiên cho sao băng đã hoàn thành chu kỳ
                 e.target.style.left = `${Math.random() * 100}vw`;
                 e.target.style.top = `${Math.random() * -20}vh`;
             }
        }, true);
    </script>

</body>
</html>
"""

# =========================================================================
# --- FLASK ROUTES ---
# =========================================================================

@app.route("/")
def intro_page():
    """Route mặc định, hiển thị trang giới thiệu (Intro)."""
    return Response(INTRO_PAGE_HTML, mimetype='text/html')

@app.route("/main")
def main_page():
    """Route trang chính sau khi Intro hoàn tất."""
    return Response(MAIN_PAGE_HTML, mimetype='text/html')

@app.route("/app.py")
def redirect_to_main():
    """Đảm bảo các liên kết cũ trỏ về trang chính."""
    return redirect(url_for('main_page'))

if __name__ == "__main__":
    app.run(debug=True)
