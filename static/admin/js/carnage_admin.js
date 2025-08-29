// Carnage Music - Custom Django Admin JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // Добавляем иконки к кнопкам
    addIconsToButtons();
    
    // Улучшаем загрузку файлов
    enhanceFileUploads();
    
    // Добавляем анимации
    addAnimations();
    
    // Улучшаем навигацию
    enhanceNavigation();
    
    // Добавляем подсказки
    addTooltips();
});

function addIconsToButtons() {
    // Добавляем иконки к кнопкам действий
    const buttons = document.querySelectorAll('.button, input[type="submit"], input[type="button"]');
    
    buttons.forEach(button => {
        const text = button.textContent || button.value;
        
        if (text.includes('Добавить') || text.includes('Add')) {
            button.innerHTML = '➕ ' + button.innerHTML;
        } else if (text.includes('Сохранить') || text.includes('Save')) {
            button.innerHTML = '💾 ' + button.innerHTML;
        } else if (text.includes('Удалить') || text.includes('Delete')) {
            button.innerHTML = '🗑️ ' + button.innerHTML;
        } else if (text.includes('Изменить') || text.includes('Change')) {
            button.innerHTML = '✏️ ' + button.innerHTML;
        }
    });
}

function enhanceFileUploads() {
    // Улучшаем интерфейс загрузки файлов
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const wrapper = document.createElement('div');
        wrapper.className = 'file-upload-wrapper';
        wrapper.style.cssText = `
            background: rgba(255, 255, 255, 0.05);
            border: 2px dashed rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            margin: 10px 0;
            transition: all 0.3s ease;
        `;
        
        const label = document.createElement('label');
        label.innerHTML = `
            <div style="font-size: 24px; margin-bottom: 10px;">📁</div>
            <div style="font-weight: 600; margin-bottom: 5px;">Выберите файл</div>
            <div style="font-size: 12px; opacity: 0.7;">или перетащите файл сюда</div>
        `;
        label.style.cssText = `
            cursor: pointer;
            display: block;
            color: #ffffff;
        `;
        
        input.style.display = 'none';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(label);
        wrapper.appendChild(input);
        
        // Обработка выбора файла
        input.addEventListener('change', function() {
            if (this.files.length > 0) {
                const file = this.files[0];
                label.innerHTML = `
                    <div style="font-size: 24px; margin-bottom: 10px;">✅</div>
                    <div style="font-weight: 600; margin-bottom: 5px;">${file.name}</div>
                    <div style="font-size: 12px; opacity: 0.7;">${(file.size / 1024 / 1024).toFixed(2)} MB</div>
                `;
                wrapper.style.borderColor = '#ff6b35';
                wrapper.style.background = 'rgba(255, 107, 53, 0.1)';
            }
        });
        
        // Drag and drop
        wrapper.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#ff6b35';
            this.style.background = 'rgba(255, 107, 53, 0.1)';
        });
        
        wrapper.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = 'rgba(255, 255, 255, 0.2)';
            this.style.background = 'rgba(255, 255, 255, 0.05)';
        });
        
        wrapper.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
}

function addAnimations() {
    // Добавляем плавные анимации для элементов
    const elements = document.querySelectorAll('.module, .form-row, .button, .object-tools a');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                entry.target.style.transition = 'all 0.6s ease';
                
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
            }
        });
    });
    
    elements.forEach(el => observer.observe(el));
}

function enhanceNavigation() {
    // Улучшаем навигацию
    const breadcrumbs = document.querySelector('.breadcrumbs');
    if (breadcrumbs) {
        breadcrumbs.style.cssText += `
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 15px 0;
        `;
    }
    
    // Добавляем индикатор загрузки
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('input[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.value;
                submitBtn.value = '⏳ Загрузка...';
                submitBtn.disabled = true;
                
                setTimeout(() => {
                    submitBtn.value = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });
}

function addTooltips() {
    // Добавляем подсказки для полей
    const fields = document.querySelectorAll('input, textarea, select');
    
    fields.forEach(field => {
        if (field.name) {
            const tooltip = document.createElement('div');
            tooltip.className = 'field-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: rgba(0, 0, 0, 0.9);
                color: white;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                z-index: 1000;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease;
                max-width: 200px;
            `;
            
            field.parentNode.style.position = 'relative';
            field.parentNode.appendChild(tooltip);
            
            field.addEventListener('focus', function() {
                const fieldName = this.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                tooltip.textContent = `Поле: ${fieldName}`;
                tooltip.style.opacity = '1';
            });
            
            field.addEventListener('blur', function() {
                tooltip.style.opacity = '0';
            });
        }
    });
}

// Добавляем уведомления
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'carnage-notification';
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #28a745, #20c997)' : 
                    type === 'error' ? 'linear-gradient(135deg, #dc3545, #fd7e14)' : 
                    'linear-gradient(135deg, #ff6b35, #f7931e)'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</span>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Глобальная функция для показа уведомлений
window.showCarnageNotification = showNotification; 