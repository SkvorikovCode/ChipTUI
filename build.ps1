# Установка зависимостей
Write-Host "Установка зависимостей..." -ForegroundColor Green
pip install -r requirements.txt

# Очистка предыдущих сборок
Write-Host "Очистка предыдущих сборок..." -ForegroundColor Green
Remove-Item -Path "dist" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "build" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "*.spec" -Exclude "build_app.spec" -ErrorAction SilentlyContinue

# Сборка приложения
Write-Host "Сборка приложения..." -ForegroundColor Green
pyinstaller build_app.spec --clean

# Проверка результата
if (Test-Path "dist/ChipTUI.exe") {
    Write-Host "Сборка успешно завершена!" -ForegroundColor Green
    Write-Host "Исполняемый файл находится в: dist/ChipTUI.exe" -ForegroundColor Green
} else {
    Write-Host "Ошибка при сборке!" -ForegroundColor Red
}   