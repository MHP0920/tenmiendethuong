// UI Components for fancy loading screens and custom dialogs

class UIComponents {
    constructor() {
        this.loadingScreen = null;
        this.dialog = null;
        this.init();
    }

    init() {
        this.createLoadingScreen();
        this.createDialog();
    }

    createLoadingScreen() {
        // Create loading screen HTML
        const loadingHTML = `
            <div id="fancyLoadingScreen" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.8);
                z-index: 9999;
                display: none;
                justify-content: center;
                align-items: center;
                backdrop-filter: blur(5px);
            ">
                <div style="
                    background: white;
                    padding: 40px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                    max-width: 300px;
                    width: 90%;
                ">
                    <div class="spinner" style="
                        width: 50px;
                        height: 50px;
                        margin: 0 auto 20px;
                        border: 4px solid #f3f3f3;
                        border-top: 4px solid #007bff;
                        border-radius: 50%;
                        animation: spin 1s linear infinite;
                    "></div>
                    <h3 id="loadingTitle" style="
                        margin: 0 0 10px 0;
                        color: #333;
                        font-size: 18px;
                    ">Đang xử lý...</h3>
                    <p id="loadingMessage" style="
                        margin: 0;
                        color: #666;
                        font-size: 14px;
                    ">Vui lòng chờ một chút</p>
                </div>
            </div>
        `;

        // Add CSS keyframes
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: scale(0.9); }
                to { opacity: 1; transform: scale(1); }
            }
            
            .loading-fade-in {
                animation: fadeIn 0.3s ease-out;
            }
        `;
        document.head.appendChild(style);

        // Add to body
        document.body.insertAdjacentHTML('beforeend', loadingHTML);
        this.loadingScreen = document.getElementById('fancyLoadingScreen');
    }

    createDialog() {
        // Create custom dialog HTML
        const dialogHTML = `
            <div id="customDialog" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 10000;
                display: none;
                justify-content: center;
                align-items: center;
                backdrop-filter: blur(3px);
            ">
                <div id="dialogContent" style="
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                    max-width: 400px;
                    width: 90%;
                    animation: fadeIn 0.3s ease-out;
                ">
                    <div id="dialogIcon" style="
                        font-size: 48px;
                        margin-bottom: 20px;
                    ">ℹ️</div>
                    <h3 id="dialogTitle" style="
                        margin: 0 0 15px 0;
                        color: #333;
                        font-size: 20px;
                    ">Thông báo</h3>
                    <p id="dialogMessage" style="
                        margin: 0 0 25px 0;
                        color: #666;
                        font-size: 16px;
                        line-height: 1.5;
                    ">Nội dung thông báo</p>
                    <div id="dialogButtons" style="
                        display: flex;
                        gap: 10px;
                        justify-content: center;
                    ">
                        <button id="dialogOk" style="
                            background: #007bff;
                            color: white;
                            border: none;
                            padding: 10px 20px;
                            border-radius: 5px;
                            cursor: pointer;
                            font-size: 14px;
                        ">OK</button>
                    </div>
                </div>
            </div>
        `;

        // Add to body
        document.body.insertAdjacentHTML('beforeend', dialogHTML);
        this.dialog = document.getElementById('customDialog');

        // Add event listeners
        document.getElementById('dialogOk').addEventListener('click', () => {
            this.hideDialog();
        });

        // Close dialog when clicking outside
        this.dialog.addEventListener('click', (e) => {
            if (e.target === this.dialog) {
                this.hideDialog();
            }
        });
    }

    showLoading(title = 'Đang xử lý...', message = 'Vui lòng chờ một chút') {
        document.getElementById('loadingTitle').textContent = title;
        document.getElementById('loadingMessage').textContent = message;
        this.loadingScreen.style.display = 'flex';
        this.loadingScreen.querySelector('div').classList.add('loading-fade-in');
    }

    hideLoading() {
        this.loadingScreen.style.display = 'none';
        this.loadingScreen.querySelector('div').classList.remove('loading-fade-in');
    }

    showDialog(options = {}) {
        const {
            title = 'Thông báo',
            message = 'Nội dung thông báo',
            type = 'info', // 'info', 'success', 'error', 'warning'
            buttons = [{ text: 'OK', action: () => this.hideDialog() }]
        } = options;

        // Set title and message
        document.getElementById('dialogTitle').textContent = title;
        document.getElementById('dialogMessage').textContent = message;

        // Set icon based on type
        const iconMap = {
            'info': 'ℹ️',
            'success': '✅',
            'error': '❌',
            'warning': '⚠️'
        };
        document.getElementById('dialogIcon').textContent = iconMap[type] || iconMap['info'];

        // Create buttons
        const buttonsContainer = document.getElementById('dialogButtons');
        buttonsContainer.innerHTML = '';
        
        buttons.forEach(button => {
            const btn = document.createElement('button');
            btn.textContent = button.text;
            btn.style.cssText = `
                background: ${button.primary ? '#007bff' : '#6c757d'};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                margin: 0 5px;
            `;
            btn.addEventListener('click', button.action);
            buttonsContainer.appendChild(btn);
        });

        this.dialog.style.display = 'flex';
    }

    hideDialog() {
        this.dialog.style.display = 'none';
    }

    // Convenience methods
    showSuccess(message, callback = null) {
        this.showDialog({
            title: 'Thành công',
            message: message,
            type: 'success',
            buttons: [{ text: 'OK', action: () => { this.hideDialog(); if (callback) callback(); } }]
        });
    }

    showError(message, callback = null) {
        this.showDialog({
            title: 'Lỗi',
            message: message,
            type: 'error',
            buttons: [{ text: 'OK', action: () => { this.hideDialog(); if (callback) callback(); } }]
        });
    }

    showWarning(message, callback = null) {
        this.showDialog({
            title: 'Cảnh báo',
            message: message,
            type: 'warning',
            buttons: [{ text: 'OK', action: () => { this.hideDialog(); if (callback) callback(); } }]
        });
    }

    showConfirm(message, onConfirm, onCancel = null) {
        this.showDialog({
            title: 'Xác nhận',
            message: message,
            type: 'warning',
            buttons: [
                { 
                    text: 'Xác nhận', 
                    primary: true,
                    action: () => { this.hideDialog(); if (onConfirm) onConfirm(); }
                },
                { 
                    text: 'Hủy', 
                    action: () => { this.hideDialog(); if (onCancel) onCancel(); }
                }
            ]
        });
    }

    // Method to handle async operations with loading
    async handleAsyncOperation(operation, loadingTitle = 'Đang xử lý...', loadingMessage = 'Vui lòng chờ một chút') {
        this.showLoading(loadingTitle, loadingMessage);
        try {
            const result = await operation();
            this.hideLoading();
            return result;
        } catch (error) {
            this.hideLoading();
            this.showError(error.message || 'Đã xảy ra lỗi không mong muốn');
            throw error;
        }
    }
}

// Initialize UI components when DOM is loaded
let uiComponents;
document.addEventListener('DOMContentLoaded', () => {
    uiComponents = new UIComponents();
});

// Global functions for easy access
function showLoading(title, message) {
    if (uiComponents) uiComponents.showLoading(title, message);
}

function hideLoading() {
    if (uiComponents) uiComponents.hideLoading();
}

function showDialog(options) {
    if (uiComponents) uiComponents.showDialog(options);
}

function showSuccess(message, callback) {
    if (uiComponents) uiComponents.showSuccess(message, callback);
}

function showError(message, callback) {
    if (uiComponents) uiComponents.showError(message, callback);
}

function showWarning(message, callback) {
    if (uiComponents) uiComponents.showWarning(message, callback);
}

function showConfirm(message, onConfirm, onCancel) {
    if (uiComponents) uiComponents.showConfirm(message, onConfirm, onCancel);
}

function handleAsyncOperation(operation, loadingTitle, loadingMessage) {
    if (uiComponents) return uiComponents.handleAsyncOperation(operation, loadingTitle, loadingMessage);
    return operation();
}
