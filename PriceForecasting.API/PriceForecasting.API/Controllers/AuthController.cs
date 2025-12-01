// Controllers/AuthController.cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PriceForecasting.Data.Context;
using PriceForecasting.Data.Models;
using BC = BCrypt.Net.BCrypt;

namespace PriceForecasting.API.Controllers;

[ApiController]
[Route("Auth")]
public class AuthController : ControllerBase
{
    private readonly AppDbContext _db;

    public AuthController(AppDbContext db)
    {
        _db = db;
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            return BadRequest(new { message = "Email и пароль обязательны" });
        }

        // Проверяем, существует ли уже пользователь
        var existingUser = await _db.users
            .FirstOrDefaultAsync(u => u.email == request.Email);

        if (existingUser != null)
        {
            return BadRequest(new { message = "Пользователь с таким email уже существует" });
        }

        // Создаем нового пользователя
        var user = new User
        {
            username = request.Email, // Используем email как username
            email = request.Email,
            password = BC.HashPassword(request.Password)
        };

        _db.users.Add(user);
        await _db.SaveChangesAsync();

        return Ok(new { message = "Регистрация успешна", userId = user.id });
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Email) || string.IsNullOrWhiteSpace(request.Password))
        {
            return BadRequest(new { message = "Email и пароль обязательны" });
        }

        // Ищем пользователя по email
        var user = await _db.users
            .FirstOrDefaultAsync(u => u.email == request.Email);

        if (user == null || !BC.Verify(request.Password, user.password))
        {
            return Unauthorized(new { message = "Неверный email или пароль" });
        }

        // В реальном проекте здесь должна быть генерация JWT токена
        // Пока возвращаем простой ответ
        return Ok(new
        {
            message = "Вход выполнен успешно",
            userId = user.id,
            email = user.email,
            username = user.username,
            token = "mock-jwt-token" // В реальном проекте генерировать настоящий JWT
        });
    }
}

public class RegisterRequest
{
    public string Email { get; set; } = default!;
    public string Password { get; set; } = default!;
}

public class LoginRequest
{
    public string Email { get; set; } = default!;
    public string Password { get; set; } = default!;
}
