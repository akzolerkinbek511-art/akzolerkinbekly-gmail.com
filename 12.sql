-- ============================================================
-- Тапсырма 12. ERD → SQL (Microsoft SQL Server / SSMS 18)
-- Онлайн тамақ жеткізу қосымшасы (FoodExpress)
-- PostgreSQL нұсқасынан T-SQL-ге бейімделген
-- ============================================================

USE master;
GO

IF DB_ID(N'FoodExpress') IS NOT NULL
BEGIN
    ALTER DATABASE FoodExpress SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE FoodExpress;
END
GO

CREATE DATABASE FoodExpress;
GO

USE FoodExpress;
GO

-- ------------------------------------------------------------
-- Пайдаланушылар
-- ------------------------------------------------------------
CREATE TABLE users (
    user_id         INT IDENTITY(1,1) PRIMARY KEY,
    email           NVARCHAR(255) NOT NULL UNIQUE,
    phone           NVARCHAR(20)  NOT NULL UNIQUE,
    password_hash   NVARCHAR(255) NOT NULL,
    full_name       NVARCHAR(150) NOT NULL,
    role            NVARCHAR(20)  NOT NULL
                    CHECK (role IN (N'customer', N'restaurant_admin', N'courier', N'admin')),
    is_active       BIT NOT NULL CONSTRAINT DF_users_is_active DEFAULT (1),
    created_at      DATETIME2(0) NOT NULL CONSTRAINT DF_users_created DEFAULT (SYSUTCDATETIME()),
    updated_at      DATETIME2(0) NOT NULL CONSTRAINT DF_users_updated DEFAULT (SYSUTCDATETIME())
);
GO

-- ------------------------------------------------------------
-- Мейрамханалар
-- ------------------------------------------------------------
CREATE TABLE restaurants (
    restaurant_id   INT IDENTITY(1,1) PRIMARY KEY,
    name            NVARCHAR(200) NOT NULL,
    address         NVARCHAR(MAX) NOT NULL,
    latitude        DECIMAL(10,8) NULL,
    longitude       DECIMAL(11,8) NULL,
    phone           NVARCHAR(20)  NULL,
    owner_id        INT NULL,
    is_active       BIT NOT NULL CONSTRAINT DF_rest_is_active DEFAULT (1),
    rating_avg      DECIMAL(3,2) NOT NULL CONSTRAINT DF_rest_rating DEFAULT (0.00),
    created_at      DATETIME2(0) NOT NULL CONSTRAINT DF_rest_created DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT FK_restaurants_owner FOREIGN KEY (owner_id) REFERENCES users(user_id)
);
GO

-- ------------------------------------------------------------
-- Мәзір категориялары
-- ------------------------------------------------------------
CREATE TABLE menu_categories (
    category_id     INT IDENTITY(1,1) PRIMARY KEY,
    restaurant_id   INT NOT NULL,
    name            NVARCHAR(100) NOT NULL,
    sort_order      INT NOT NULL CONSTRAINT DF_cat_sort DEFAULT (0),
    CONSTRAINT FK_categories_restaurant FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id) ON DELETE CASCADE
);
GO

-- ------------------------------------------------------------
-- Тағамдар
-- ------------------------------------------------------------
CREATE TABLE dishes (
    dish_id              INT IDENTITY(1,1) PRIMARY KEY,
    category_id          INT NOT NULL,
    name                 NVARCHAR(200) NOT NULL,
    description          NVARCHAR(MAX) NULL,
    price                DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    image_url            NVARCHAR(500) NULL,
    is_available         BIT NOT NULL CONSTRAINT DF_dish_available DEFAULT (1),
    preparation_time_min INT NOT NULL CONSTRAINT DF_dish_prep DEFAULT (15),
    CONSTRAINT FK_dishes_category FOREIGN KEY (category_id)
        REFERENCES menu_categories(category_id) ON DELETE CASCADE
);
GO

-- ------------------------------------------------------------
-- Тапсырыстар
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id         INT IDENTITY(1,1) PRIMARY KEY,
    customer_id      INT NOT NULL,
    restaurant_id    INT NOT NULL,
    courier_id       INT NULL,
    status           NVARCHAR(30) NOT NULL CONSTRAINT DF_order_status DEFAULT (N'new')
                     CHECK (status IN (N'new', N'paid', N'preparing', N'ready',
                                       N'on_the_way', N'delivered', N'cancelled', N'returned')),
    total_amount     DECIMAL(12,2) NOT NULL,
    delivery_address NVARCHAR(MAX) NOT NULL,
    delivery_fee     DECIMAL(8,2) NOT NULL CONSTRAINT DF_order_fee DEFAULT (0),
    promo_code       NVARCHAR(50) NULL,
    discount_amount  DECIMAL(10,2) NOT NULL CONSTRAINT DF_order_discount DEFAULT (0),
    created_at       DATETIME2(0) NOT NULL CONSTRAINT DF_order_created DEFAULT (SYSUTCDATETIME()),
    updated_at       DATETIME2(0) NOT NULL CONSTRAINT DF_order_updated DEFAULT (SYSUTCDATETIME()),
    delivered_at     DATETIME2(0) NULL,
    CONSTRAINT FK_orders_customer   FOREIGN KEY (customer_id)   REFERENCES users(user_id),
    CONSTRAINT FK_orders_restaurant FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id),
    CONSTRAINT FK_orders_courier    FOREIGN KEY (courier_id)    REFERENCES users(user_id)
);
GO

-- ------------------------------------------------------------
-- Тапсырыс элементтері
-- ------------------------------------------------------------
CREATE TABLE order_items (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id      INT NOT NULL,
    dish_id       INT NOT NULL,
    quantity      INT NOT NULL CHECK (quantity > 0),
    unit_price    DECIMAL(10,2) NOT NULL,
    notes         NVARCHAR(MAX) NULL,
    CONSTRAINT FK_order_items_order FOREIGN KEY (order_id)
        REFERENCES orders(order_id) ON DELETE CASCADE,
    CONSTRAINT FK_order_items_dish  FOREIGN KEY (dish_id)
        REFERENCES dishes(dish_id)
);
GO

-- ------------------------------------------------------------
-- Төлемдер
-- ------------------------------------------------------------
CREATE TABLE payments (
    payment_id     INT IDENTITY(1,1) PRIMARY KEY,
    order_id       INT NOT NULL UNIQUE,
    amount         DECIMAL(12,2) NOT NULL,
    method         NVARCHAR(30) NOT NULL
                   CHECK (method IN (N'card', N'kaspi', N'cash')),
    status         NVARCHAR(20) NOT NULL CONSTRAINT DF_pay_status DEFAULT (N'pending')
                   CHECK (status IN (N'pending', N'completed', N'failed', N'refunded')),
    transaction_id NVARCHAR(100) NULL,
    paid_at        DATETIME2(0) NULL,
    CONSTRAINT FK_payments_order FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
GO

-- ------------------------------------------------------------
-- Рейтингтер
-- ------------------------------------------------------------
CREATE TABLE ratings (
    rating_id      INT IDENTITY(1,1) PRIMARY KEY,
    order_id       INT NOT NULL,
    from_user_id   INT NOT NULL,
    to_entity_type NVARCHAR(20) NOT NULL
                   CHECK (to_entity_type IN (N'restaurant', N'courier')),
    to_entity_id   INT NOT NULL,
    score          SMALLINT NOT NULL CHECK (score BETWEEN 1 AND 5),
    comment        NVARCHAR(MAX) NULL,
    created_at     DATETIME2(0) NOT NULL CONSTRAINT DF_rating_created DEFAULT (SYSUTCDATETIME()),
    CONSTRAINT FK_ratings_order FOREIGN KEY (order_id) REFERENCES orders(order_id),
    CONSTRAINT FK_ratings_user  FOREIGN KEY (from_user_id) REFERENCES users(user_id)
);
GO

-- ------------------------------------------------------------
-- Промокодтар
-- ------------------------------------------------------------
CREATE TABLE promo_codes (
    promo_id         INT IDENTITY(1,1) PRIMARY KEY,
    code             NVARCHAR(50) NOT NULL UNIQUE,
    discount_type    NVARCHAR(20) NOT NULL
                     CHECK (discount_type IN (N'percent', N'fixed')),
    discount_value   DECIMAL(10,2) NOT NULL,
    min_order_amount DECIMAL(10,2) NOT NULL CONSTRAINT DF_promo_min DEFAULT (0),
    max_uses         INT NULL,
    used_count       INT NOT NULL CONSTRAINT DF_promo_used DEFAULT (0),
    valid_from       DATETIME2(0) NULL,
    valid_to         DATETIME2(0) NULL,
    is_active        BIT NOT NULL CONSTRAINT DF_promo_active DEFAULT (1)
);
GO

-- ------------------------------------------------------------
-- Индекстер
-- ------------------------------------------------------------
CREATE INDEX IX_orders_customer    ON orders(customer_id);
CREATE INDEX IX_orders_status      ON orders(status);
CREATE INDEX IX_orders_restaurant  ON orders(restaurant_id);
CREATE INDEX IX_dishes_category    ON dishes(category_id);
CREATE INDEX IX_restaurants_latlon ON restaurants(latitude, longitude);
GO

-- ------------------------------------------------------------
-- Кестелерге түсініктеме (extended properties)
-- ------------------------------------------------------------
EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Жүйе пайдаланушылары (тұтынушы, мейрамхана, жеткізуші, админ)',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'users';
GO

EXEC sp_addextendedproperty
    @name = N'MS_Description', @value = N'Тапсырыстар және олардың мәртебесі. State machine: new → paid → preparing → ready → on_the_way → delivered',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'orders';
GO

PRINT N'FoodExpress схемасы сәтті жасалды (SQL Server).';
GO
