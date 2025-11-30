FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build

WORKDIR /src

# 1. Копируем ВСЕ файлы решения
COPY . .

# 2. Восстанавливаем и публикуем через solution file
RUN dotnet restore "PriceForecasting.API/PriceForecastingSystem.sln"
RUN dotnet publish "PriceForecasting.API/PriceForecasting.API/PriceForecasting.API.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "PriceForecasting.API.dll"]