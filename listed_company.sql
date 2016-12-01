/*
Navicat MySQL Data Transfer

Source Server         : local_mysql
Source Server Version : 50634
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50634
File Encoding         : 65001

Date: 2016-12-01 16:07:36
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for listed_company
-- ----------------------------
DROP TABLE IF EXISTS `listed_company`;
CREATE TABLE `listed_company` (
  `id` int(6) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `companyCode` char(6) CHARACTER SET latin1 DEFAULT NULL,
  `companyShortName` varchar(100) DEFAULT NULL,
  `companyName` varchar(200) DEFAULT NULL,
  `companyEnlishName` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `ipoAddress` varchar(200) DEFAULT NULL,
  `aSharesCode` char(6) CHARACTER SET latin1 DEFAULT NULL,
  `aSharesShortName` varchar(100) DEFAULT NULL,
  `aSharesIPODate` varchar(19) CHARACTER SET latin1 DEFAULT NULL,
  `aSharesTotalCapital` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `aSharesOutstandingCaptial` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `bSharesCode` char(6) CHARACTER SET latin1 DEFAULT NULL,
  `bSharesShortName` varchar(100) DEFAULT NULL,
  `bSharesIPODate` varchar(19) CHARACTER SET latin1 DEFAULT NULL,
  `bSharesTotalCapital` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `bSharesOutstandingCaptial` varchar(20) CHARACTER SET latin1 DEFAULT NULL,
  `area` varchar(20) DEFAULT NULL,
  `province` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `trade` varchar(20) DEFAULT NULL,
  `website` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `status` char(1) CHARACTER SET latin1 DEFAULT '1' COMMENT '1 上市\r\n\r\n0 退市',
  `exitDate` varchar(10) CHARACTER SET latin1 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `companyCodeIndex` (`companyCode`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=3304 DEFAULT CHARSET=utf8;
