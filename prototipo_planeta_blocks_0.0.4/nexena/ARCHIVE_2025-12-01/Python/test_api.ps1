# Script de prueba para la API de autenticación
# Asegúrate de que la app está corriendo en http://127.0.0.1:5000/

$BASE_URL = "http://127.0.0.1:5000"
$HEADERS = @{"Content-Type" = "application/json"}

Write-Host "=== Pruebas de API de Autenticación ===" -ForegroundColor Cyan

# 1. Health check
Write-Host "`n1. Health Check" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "$BASE_URL/api/health" -Method Get -Headers $HEADERS
Write-Host ($response | ConvertTo-Json)

# 2. Login con usuario demo
Write-Host "`n2. Login (usuario: demo, password: Password123)" -ForegroundColor Yellow
$loginData = @{
    username = "demo"
    password = "Password123"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/login" -Method Post -Body $loginData -Headers $HEADERS
Write-Host ($response | ConvertTo-Json)

# 3. Obtener usuario actual (requiere sesión)
Write-Host "`n3. Obtener usuario actual" -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/me" -Method Get -Headers $HEADERS
    Write-Host ($response | ConvertTo-Json)
} catch {
    Write-Host "Error: $_"
}

# 4. Registrar nuevo usuario
Write-Host "`n4. Registrar nuevo usuario" -ForegroundColor Yellow
$registerData = @{
    username = "newuser"
    email = "newuser@example.com"
    password = "Test1234"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/register" -Method Post -Body $registerData -Headers $HEADERS
Write-Host ($response | ConvertTo-Json)

# 5. Recuperar username
Write-Host "`n5. Recuperar username (email: demo@example.com)" -ForegroundColor Yellow
$forgotUserData = @{
    email = "demo@example.com"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/forgot-username" -Method Post -Body $forgotUserData -Headers $HEADERS
Write-Host ($response | ConvertTo-Json)

# 6. Solicitar reset de contraseña
Write-Host "`n6. Solicitar reset de contraseña (usuario: demo)" -ForegroundColor Yellow
$forgotPwData = @{
    username = "demo"
} | ConvertTo-Json
$response = Invoke-RestMethod -Uri "$BASE_URL/api/auth/forgot-password" -Method Post -Body $forgotPwData -Headers $HEADERS
$resetToken = $response.reset_token
Write-Host ($response | ConvertTo-Json)

# 7. Listar usuarios
Write-Host "`n7. Listar todos los usuarios" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "$BASE_URL/api/users" -Method Get -Headers $HEADERS
Write-Host ($response | ConvertTo-Json)

Write-Host "`n=== Pruebas finalizadas ===" -ForegroundColor Cyan
