import datetime
from flask_mysqldb import MySQL
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)




app.config['MYSQL_HOST'] = 'flask.cgz5vmvv53yv.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PORT'] = 3305
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)


@app.route('/')
def index():
    cur = mysql.connection.cursor()

    cur.execute('''CREATE TABLE `cache` (
        `id` int(10) NOT NULL,
        `capacity` varchar(20) DEFAULT NULL,
        `policy` int(11) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4''')

    cur.execute('''CREATE TABLE `cacheinformation` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `datetime` datetime(6) NOT NULL DEFAULT current_timestamp(6) ON UPDATE current_timestamp(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4''')

    cur.execute('''INSERT INTO `cacheinformation` (`id`, `name`, `description`, `datetime`) VALUES
(1, 'Least Recently Used', 'Discards the least recently used keys first. This algorithm requires keeping track of\r\nwhat was used when, if one wants to make sure the algorithm always discards the\r\nleast recently used key.', '2022-10-18 14:45:39.000000'),
(2, 'Random Replacement', 'Randomly selects a key and discards it to make space when necessary.\r\nThis algorithm does not require keeping any information about the access\r\nhistory.', '2022-10-18 14:48:22.000000')''')

    cur.execute('''CREATE TABLE `statistics` (
  `id` int(100) NOT NULL,
  `MissRate` int(100) NOT NULL,
  `HitRate` int(100) NOT NULL,
  `NumberOfItems` int(100) NOT NULL,
  `CacheCapacity` int(100) NOT NULL,
  `NumberOfReq` int(100) NOT NULL,
  `DateTime` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;''')

    cur.execute('''CREATE TABLE `uploadedfiles` (
  `uniquekeys` text NOT NULL,
  `direction` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
''')

    cur.execute('''ALTER TABLE `cache`
  ADD PRIMARY KEY (`id`),
  ADD KEY `policy` (`policy`),
  ADD KEY `id` (`id`);''')

    cur.execute('''ALTER TABLE `cacheinformation`
  ADD PRIMARY KEY (`id`);''')
    

    cur.execute('''ALTER TABLE `statistics`
  ADD KEY `id` (`id`) USING BTREE;''')

    cur.execute('''ALTER TABLE `cache`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;
    ''')

    cur.execute('''ALTER TABLE `statistics`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=974;
    ''')

    cur.execute('''ALTER TABLE `cache`
  ADD CONSTRAINT `cache_ibfk_1` FOREIGN KEY (`policy`) REFERENCES `cacheinformation` (`id`);
COMMIT;
    ''')
    #cur.execute('''ALTER TABLE config
    #ADD CONSTRAINT config_ibfk_1 FOREIGN KEY (policty) REFERENCES replacement (id)''')

    #cur.execute('''
    #INSERT INTO `replacement`(`id`, `policty`, `description`)
    #VALUES(1, 'random', 'Random replacement a') ; ''')
    #cur.execute('''INSERT INTO `replacement`(`id`, `policty`, `description`)
    #VALUES(2, 'LRU', 'The least recently u') ;''')


    result = cur.fetchall()
    print(result)




    mysql.connection.commit()
    cur.close()

    return 'Hello, World!'
if __name__ == '__main__':
    app.run(debug=False) 







