import subprocess

def install_glpi():
    # mise à jour
    subprocess.run(["apt-get", "update", "&&", "apt-get", "upgrade"])
    # Téléchargement de l'archive GLPI
    subprocess.run(["wget", "https://github.com/glpi-project/glpi/releases/download/9.5.7/glpi-9.5.7.tgz"])

    # Extraction de l'archive
    subprocess.run(["tar", "-xvzf", "glpi-9.5.7.tgz"])

    # Déplacement des fichiers dans le répertoire de destination
    subprocess.run(["mv", "glpi", "/var/www/html/glpi"])

    # Configuration des permissions
    subprocess.run(["chown", "-R", "www-data:www-data", "/var/www/html/glpi"])
    subprocess.run(["chmod", "-R", "755", "/var/www/html/glpi"])

    # Installation des dépendances PHP
    subprocess.run(["apt-get", "install", "-y", "php7.4-curl", "php7.4-gd", "php7.4-mbstring", "php7.4-xml", "apache2", "mysql-server"])

    # Restart Apache et mysql service
    subprocess.run(["service", "apache2", "restart"])
    subprocess.run(["service", "mysql", "restart"])

    # Configuration du serveur web (Apache)
    subprocess.run(["a2enmod", "rewrite"])
    subprocess.run(["systemctl", "restart", "apache2"])

    # Configuration de la base de données MySQL/MariaDB
    subprocess.run(["mysql", "-u", "root", "-e", "CREATE DATABASE glpidb"])
    subprocess.run(["mysql", "-u", "root", "-e", "GRANT ALL PRIVILEGES ON glpidb.* TO 'glpiuser'@'localhost' IDENTIFIED BY 'glpipassword'"])
    subprocess.run(["mysql", "-u", "root", "glpidb", "-e", "SOURCE /var/www/html/glpi/install/mysql/glpi-empty-db.sql"])

    # Configuration finale de GLPI
    subprocess.run(["cp", "/var/www/html/glpi/config/config_sample.inc.php", "/var/www/html/glpi/config/config.inc.php"])
    subprocess.run(["chmod", "777", "/var/www/html/glpi/config/config.inc.php"])

    print("Installation de GLPI terminée.")

# Appel de la fonction d'installation
install_glpi()
