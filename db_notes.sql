
DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL COMMENT '账号，一般是手机号',
  `password` varchar(45) NOT NULL,
  `avatar` varchar(128) DEFAULT NULL,
  `leader_uid` bigint(20) DEFAULT '0',
  `show_name` varchar(128) DEFAULT NULL,
  `title` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8 COMMENT='用户账号密码';



DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `uid` bigint(20) unsigned NOT NULL,
  `token` varchar(45) NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `expire_time` int(10) unsigned NOT NULL,
  KEY `FK_token_uid` (`uid`),
  CONSTRAINT `FK_token_uid` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `id` varchar(128) NOT NULL,
  `uid` bigint(20) unsigned NOT NULL,
  `name` varchar(128) NOT NULL,
  `group_name` text NOT NULL,
  `spell` text NOT NULL,
  `address` text NOT NULL,
  `longitude` varchar(128) NOT NULL,
  `latitude` varchar(128) NOT NULL,
  `boss` varchar(128) DEFAULT NULL,
  `phone` varchar(128) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `description` longtext,
  `update_date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `is_deleted` bigint(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_customer_user` (`uid`),
  CONSTRAINT `FK_customer_user` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groups` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) unsigned NOT NULL,
  `group_name` varchar(128) NOT NULL,
  `update_date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `is_deleted` bigint(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_groups_user` (`uid`),
  CONSTRAINT `FK_groups_user` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;



DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notes` (
  `id` varchar(128) NOT NULL,
  `uid` bigint(20) unsigned NOT NULL,
  `date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `update_date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `customer_id` varchar(128) NOT NULL,
  `thumbnail` text,
  `pic` text,
  `address` text NOT NULL,
  `longitude` varchar(128) NOT NULL,
  `latitude` varchar(128) NOT NULL,
  `note` longtext NOT NULL,
  `repost_from` varchar(128) NOT NULL DEFAULT '0' COMMENT 'this note may repost from others',
  `is_deleted` bigint(10) unsigned NOT NULL DEFAULT '0',
  `public_to` text NOT NULL COMMENT '设置笔记允许哪些人看, 每个ID间用逗号隔开',
  PRIMARY KEY (`id`),
  KEY `FK_notes_user` (`uid`),
  KEY `FK_notes_customer` (`customer_id`),
  CONSTRAINT `FK_notes_customer` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_notes_user` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `alarm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarm` (
  `id` varchar(128) NOT NULL,
  `uid` bigint(20) unsigned NOT NULL,
  `note_id` varchar(128) NOT NULL,
  `date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `update_date` bigint(20) unsigned NOT NULL DEFAULT '0',
  `is_deleted` bigint(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `FK_alarm_user` (`uid`),
  KEY `FK_alarm_notes` (`note_id`),
  CONSTRAINT `FK_alarm_notes` FOREIGN KEY (`note_id`) REFERENCES `notes` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_alarm_user` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP VIEW IF EXISTS `view_user`;

create VIEW `view_user` AS select `a`.`id` AS `id`,`a`.`user_name` AS `user_name`,`a`.`password` AS `password`,`b`.`token` AS `token`,`b`.`create_time` AS `create_time`,`b`.`expire_time` AS `expire_time`,`a`.`avatar` AS `avatar`,`a`.`leader_uid` AS `leader_uid`,`a`.`show_name` AS `show_name`,`a`.`title` AS `title` from (`user` `a` left join `token` `b` on((`a`.`id` = `b`.`uid`)));


create VIEW `view_user_with_leader` AS select `a`.`id` AS `id`,`a`.`user_name` AS `user_name`,`a`.`password` AS `password`,`a`.`token` AS `token`,`a`.`create_time` AS `create_time`,`a`.`expire_time` AS `expire_time`,`a`.`avatar` AS `avatar`,`a`.`leader_uid` AS `leader_uid`,`a`.`show_name` AS `show_name`,`a`.`title` AS `title`,`b`.`show_name` AS `leader_name`,`b`.`title` AS `leader_title` from (`view_user` `a` left join `user` `b` on((`a`.`id` = `b`.`id`)));


create VIEW `view_notes` AS select `a`.`id` AS `id`,`a`.`uid` AS `uid`,`a`.`date` AS `date`,`a`.`update_date` AS `update_date`,`a`.`customer_id` AS `customer_id`,`b`.`name` AS `customer_name`,`a`.`address` AS `address`,`a`.`longitude` AS `longitude`,`a`.`latitude` AS `latitude`,`a`.`note` AS `note`,`a`.`thumbnail` AS `thumbnail`,`a`.`pic` AS `pic`,`a`.`is_deleted` AS `is_deleted`,`a`.`repost_from` AS `repost_from`,`c`.`avatar` AS `avatar`,`c`.`show_name` AS `author` from ((`notes` `a` left join `customer` `b` on((`a`.`customer_id` = `b`.`id`))) left join `user` `c` on((`a`.`uid` = `c`.`id`)));


