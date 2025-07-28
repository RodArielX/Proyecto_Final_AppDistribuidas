CREATE DATABASE IF NOT EXISTS inventario;
USE inventario;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    codigo VARCHAR(50) UNIQUE,
    descripcion TEXT,
    unidad VARCHAR(50),
    categoria VARCHAR(100)
);

INSERT INTO usuarios (email, password) VALUES ('admin@gmail.com', '1234');

-- Crear usuario de replicación
CREATE USER 'replicador'@'%' IDENTIFIED BY 'replica123';
GRANT REPLICATION SLAVE ON *.* TO 'replicador'@'%';
FLUSH PRIVILEGES;

