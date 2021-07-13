-- MySQL dump 10.13  Distrib 5.7.9, for Win64 (x86_64)
--
-- Host: localhost    Database: dialogue_robot
-- ------------------------------------------------------
-- Server version	5.7.10-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `q_a`
--

DROP TABLE IF EXISTS `q_a`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `q_a` (
  `idQandA` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(255) DEFAULT NULL,
  `answer` longtext,
  PRIMARY KEY (`idQandA`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='问题和答案';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `q_a`
--

LOCK TABLES `q_a` WRITE;
/*!40000 ALTER TABLE `q_a` DISABLE KEYS */;
INSERT INTO `q_a` VALUES (1,'随便什么问题','答案'),(2,'第二个问题','的答案');
/*!40000 ALTER TABLE `q_a` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_password` varchar(45) DEFAULT NULL,
  `user_phone` char(11) DEFAULT NULL,
  `user_pic` varchar(255) DEFAULT NULL,
  `user_gender` varchar(45) DEFAULT NULL,
  `user_site` tinytext,
  `user_level` int(11) DEFAULT NULL,
  `user_pallow` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'张三','12345678','12345678910','P5SHNENc.jpg','男','北京化工大学昌平校区某某栋楼某某宿舍',3,1),(3,'王五','123456789','10100000000','N6PJPxpb.jpg','女','',2,1),(7,'啊啊啊kkkaaa','123456789','10100000000','rMVFza0m.jpg','男','三生三世',3,1),(8,'测试添加','87654321','10100003000','4ynhfgdU.jpg','男','北京化工大学昌平校区某某栋某宿舍',1,1),(9,'王五2','12345678','10100003000','TBtOCthx.jpg','男','北京化工大学昌平校区某某栋某宿舍',1,1),(11,'李四22','12345678','10100003000','EPGta5jB.jpg','男','北京化工大学昌平校区某某栋某宿舍',1,1),(12,'李四33','123456789','10100000001','MPc9QuIh.jpg','男','北京化工大学昌平校区某某栋某宿舍',1,1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-07-09 10:42:45
