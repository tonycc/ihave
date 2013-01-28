SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+8:00";
ALTER DATABASE CHARACTER SET "utf8";


DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    uid VARCHAR(20) NOT NULL UNIQUE,
    username VARCHAR(100),
    province VARCHAR(10),
    city VARCHAR(10),
    location VARCHAR(10),
    gender VARCHAR(10),
    profile_image_url VARCHAR(50),
    verified VARCHAR(10),
    followers_count VARCHAR(10),
    friends_count VARCHAR(10),
    avatar_large VARCHAR(100),
    verified_reason VARCHAR(200),
    bi_followers_count VARCHAR(10)
);