-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'docker_machine'
-- schema of docker machine
-- ---

DROP TABLE IF EXISTS `docker_machine`;
		
CREATE TABLE `docker_machine` (
  `id` INTEGER NOT NULL AUTO_INCREMENT DEFAULT NULL,
  `hostname` VARCHAR(64) NULL DEFAULT NULL,
  `ip_addr` VARCHAR(15) NOT NULL DEFAULT 'NULL',
  `interfaces` SET NULL DEFAULT NULL,
  `labels` SET NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT 'schema of docker machine';

-- ---
-- Table 'macvlan_interface'
-- schema of macvlan interface
-- ---

DROP TABLE IF EXISTS `macvlan_interface`;
		
CREATE TABLE `macvlan_interface` (
  `id` INTEGER NULL AUTO_INCREMENT DEFAULT NULL,
  `name` VARCHAR(32) NOT NULL DEFAULT 'NULL',
  `machine_id` INTEGER NOT NULL DEFAULT NULL,
  `subnet` VARCHAR(18) NOT NULL DEFAULT '192.168.0.1/24',
  `min_vlan` INTEGER NOT NULL DEFAULT 1,
  `max_vlan` INTEGER NOT NULL DEFAULT 4094,
  `labels` SET NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) COMMENT 'schema of macvlan interface';

-- ---
-- Table 'label'
-- schema of label for marking resource instance
-- ---

DROP TABLE IF EXISTS `label`;
		
CREATE TABLE `label` (
  `id` INTEGER NOT NULL AUTO_INCREMENT DEFAULT NULL,
  `name` VARCHAR(64) NOT NULL DEFAULT 'NULL',
  `desc` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`id`)
) COMMENT 'schema of label for marking resource instance';

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `docker_machine` ADD FOREIGN KEY (interfaces) REFERENCES `label` (`id`);
ALTER TABLE `macvlan_interface` ADD FOREIGN KEY (machine_id) REFERENCES `docker_machine` (`id`);
ALTER TABLE `macvlan_interface` ADD FOREIGN KEY (labels) REFERENCES `label` (`id`);

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `docker_machine` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `macvlan_interface` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `label` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `docker_machine` (`id`,`hostname`,`ip_addr`,`interfaces`,`labels`) VALUES
-- ('','','','','');
-- INSERT INTO `macvlan_interface` (`id`,`name`,`machine_id`,`subnet`,`min_vlan`,`max_vlan`,`labels`) VALUES
-- ('','','','','','','');
-- INSERT INTO `label` (`id`,`name`,`desc`) VALUES
-- ('','','');
