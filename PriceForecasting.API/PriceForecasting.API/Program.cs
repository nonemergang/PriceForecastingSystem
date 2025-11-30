using Microsoft.EntityFrameworkCore;
using Microsoft.OpenApi.Models;
using PriceForecasting.Data.Context;

var builder = WebApplication.CreateBuilder(args);

// ✅ ДОБАВЬТЕ CORS ПОЛИТИКУ
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowGitHubPages", policy =>
    {
        policy.WithOrigins(
                "https://urfu-priceforecast.github.io",  // Ваш GitHub Pages
                "http://localhost:3000",                 // Локальная разработка
                "https://localhost:3000"                 // Локальная разработка HTTPS
            )
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials();
    });
});

builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.PropertyNamingPolicy = null;
    });

builder.Services.AddSwaggerGen(c =>
{
    c.SwaggerDoc("v1", new OpenApiInfo { Title = "PriceForecasting API", Version = "v1" });
});

// DbContext
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Добавляем MemoryCache (для кеширования рекомендаций 6 часов)
builder.Services.AddMemoryCache();

var app = builder.Build();

// ✅ ИСПОЛЬЗУЙТЕ CORS (добавьте эту строку)
app.UseCors("AllowGitHubPages");

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();
app.Run();