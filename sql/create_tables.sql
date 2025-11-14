USE monitor;

CREATE TABLE IF NOT EXISTS monitoring_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_origem VARCHAR(45) NOT NULL,
    ip_destino VARCHAR(45) NOT NULL,
    uso_memoria FLOAT NOT NULL,
    uso_cpu FLOAT NOT NULL,
    uso_disco FLOAT NOT NULL,
    processos TEXT NOT NULL,
    tempo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tempo (tempo),
    INDEX idx_ip_origem (ip_origem)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
