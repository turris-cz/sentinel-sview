INSERT INTO identity (sn, device_token) VALUES
 ('0000000000000001', '1000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000002', '2000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000003', '3000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000004', '4000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000005', '5000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000006', '6000000000000000000000000000000000000000000000000000000000000001'),
 ('0000000000000007', '7000000000000000000000000000000000000000000000000000000000000001')
ON CONFLICT (sn, device_token) DO NOTHING;

INSERT INTO incidents VALUES
    (NOW(), 1, 1, 'minipot_ftp', 'connect', '192.0.2.1', 'CZ'),
    (NOW(), 1, 1, 'minipot_ftp', 'connect', '198.51.100.10', 'CZ'),
    (NOW(), 2, 1, 'minipot_smtp', 'connect', '192.0.2.12', 'CZ'),
    (NOW() - INTERVAL '5 minutes', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '10 minutes', 2, 2, 'minipot_http', 'connect', '192.0.2.15', 'CZ'),
    (NOW() - INTERVAL '20 minutes', 1, 4, 'minipot_http', 'login', '203.0.113.212', 'GB'),
    (NOW() - INTERVAL '40 minutes', 1, 4, 'fwlogs', 'small_port_scan', '192.0.2.1', 'CZ'),
    (NOW() - INTERVAL '40 minutes', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'CZ'),
    (NOW() - INTERVAL '1 hour', 1, 1, 'fwlogs', 'big_port_scan', '192.0.2.1', 'SK'),
    (NOW() - INTERVAL '3 hours', 1, 1, 'minipot_ftp', 'connect', '192.0.2.1', 'US'),
    (NOW() - INTERVAL '6 hours', 1, 1, 'minipot_ftp', 'connect', '198.51.100.11', 'US'),
    (NOW() - INTERVAL '6 hours', 1, 1, 'minipot_ftp', 'connect', '198.51.100.12', 'DE'),
    (NOW() - INTERVAL '6 hours', 1, 1, 'minipot_ftp', 'connect', '198.51.100.13', 'DE'),
    (NOW() - INTERVAL '7 hours', 1, 1, 'minipot_smtp', 'connect', '192.0.2.12', 'US'),
    (NOW() - INTERVAL '7 hours', 1, 1, 'minipot_smtp', 'connect', '192.0.2.13', 'FR'),
    (NOW() - INTERVAL '7 hours', 1, 1, 'minipot_smtp', 'connect', '192.0.2.14', 'FR'),
    (NOW() - INTERVAL '10 hours', 2, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'CN'),
    (NOW() - INTERVAL '12 hours', 2, 2, 'minipot_http', 'connect', '192.0.2.15', 'CN'),
    (NOW() - INTERVAL '15 hours', 2, 4, 'minipot_http', 'login', '203.0.113.212', 'CN'),
    (NOW() - INTERVAL '20 hours', 2, 4, 'fwlogs', 'small_port_scan', '192.0.2.1', 'US'),
    (NOW() - INTERVAL '1 day', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'US'),
    (NOW() - INTERVAL '2 days', 1, 1, 'fwlogs', 'big_port_scan', '192.0.2.1', 'CN'),
    (NOW() - INTERVAL '5 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '5 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '5 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '7 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '7 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'SK'),
    (NOW() - INTERVAL '10 days', 1, 2, 'minipot_http', 'connect', '192.0.2.15', 'CZ'),
    (NOW() - INTERVAL '20 days', 1, 4, 'minipot_http', 'login', '203.0.113.212', 'GB'),
    (NOW() - INTERVAL '1 month', 1, 1, 'fwlogs', 'big_port_scan', '192.0.2.1', 'SK'),
    (NOW() - INTERVAL '40 days', 1, 4, 'fwlogs', 'small_port_scan', '192.0.2.1', 'CZ'),
    (NOW() - INTERVAL '40 days', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'CZ'),
    (NOW() - INTERVAL '2 months', 1, 1, 'minipot_ftp', 'connect', '192.0.2.1', 'US'),
    (NOW() - INTERVAL '60 days', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'CZ'),
    (NOW() - INTERVAL '60 days', 1, 1, 'minipot_ftp', 'connect', '198.51.100.10', 'US'),
    (NOW() - INTERVAL '60 days', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'CZ'),
    (NOW() - INTERVAL '60 days', 1, 1, 'minipot_ftp', 'connect', '198.51.100.10', 'US'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.12', 'US'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.12', 'US'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.12', 'US'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.15', 'TW'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.15', 'TW'),
    (NOW() - INTERVAL '70 days', 1, 1, 'minipot_smtp', 'connect', '192.0.2.15', 'TW'),
    (NOW() - INTERVAL '80 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'CN'),
    (NOW() - INTERVAL '80 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'CN'),
    (NOW() - INTERVAL '80 days', 1, 2, 'minipot_telnet', 'connect', '203.0.113.58', 'CN'),
    (NOW() - INTERVAL '3 months', 1, 2, 'minipot_http', 'connect', '192.0.2.15', 'CN'),
    (NOW() - INTERVAL '4 months', 1, 4, 'minipot_http', 'login', '203.0.113.212', 'CN'),
    (NOW() - INTERVAL '5 months', 1, 4, 'fwlogs', 'small_port_scan', '192.0.2.1', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.2', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.5', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.6', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.7', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.8', 'US'),
    (NOW() - INTERVAL '6 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.9', 'US'),
    (NOW() - INTERVAL '7 months', 1, 4, 'fwlogs', 'big_port_scan', '192.0.2.9', 'US'),
    (NOW() - INTERVAL '11 months', 1, 1, 'fwlogs', 'big_port_scan', '192.0.2.1', 'CN');

INSERT INTO passwords VALUES
    (NOW(), 1, 'username', 'password'),
    (NOW(), 1, 'username', 'passw0rd'),
    (NOW() - INTERVAL '5 minutes', 1, 'jmeno', 'heslo'),
    (NOW() - INTERVAL '20 minutes', 1, 'xxx', 'xxx'),
    (NOW() - INTERVAL '2 hours', 1, 'user', 'secret'),
    (NOW() - INTERVAL '1 day', 1, 'username', 'password'),
    (NOW() - INTERVAL '1 day', 1, 'username', 'passw0rd'),
    (NOW() - INTERVAL '70 days', 1, 'jmeno', 'heslo'),
    (NOW() - INTERVAL '2 months', 1, 'xxx', 'xxx'),
    (NOW() - INTERVAL '4 months', 1, 'user', 'secret');

INSERT INTO ports VALUES
    (NOW(), 1, 21, 'TCP'),
    (NOW(), 1, 22, 'TCP'),
    (NOW() - INTERVAL '5 minutes', 1, 22, 'TCP'),
    (NOW() - INTERVAL '10 minutes', 1, 25, 'TCP'),
    (NOW() - INTERVAL '30 minutes', 1, 53, 'TCP'),
    (NOW() - INTERVAL '30 minutes', 1, 53, 'UDP'),
    (NOW() - INTERVAL '50 minutes', 1, 443, 'TCP'),
    (NOW() - INTERVAL '70 minutes', 1, 1194, 'UDP'),
    (NOW() - INTERVAL '80 minutes', 1, 21, 'TCP'),
    (NOW() - INTERVAL '2 hours', 1, 22, 'TCP'),
    (NOW() - INTERVAL '10 hours', 1, 22, 'TCP'),
    (NOW() - INTERVAL '2 days', 1, 25, 'TCP'),
    (NOW() - INTERVAL '1 months', 1, 53, 'TCP'),
    (NOW() - INTERVAL '4 months', 1, 53, 'UDP'),
    (NOW() - INTERVAL '4 months', 1, 443, 'TCP'),
    (NOW() - INTERVAL '4 months', 1, 1194, 'UDP');

INSERT INTO passwords_pwned VALUES
    (1, 'c90c6d6b15abf94a553dca2d36e7d80c500ad329', 49, ARRAY ['smtp']::data_source[]),
    (2, 'a153ba7319d815ada7f473a54c209b4e7c9e3836', 29, ARRAY ['haas', 'telnet']::data_source[]),
    (3, '8f263db9e9e6e7259866281db399e16fac312bbb', 63, ARRAY ['haas']::data_source[]),
    (4, '6e017b5464f820a6c1bb5e9f6d711a667a80d8ea', 143, ARRAY ['telnet', 'haas']::data_source[]),
    (5, 'dd3027b0b171b836ce6822b2d46601210f9a67e6', 80, ARRAY ['ftp', 'telnet']::data_source[]),
    (6, '079e0628ed2e3ce337d48ed7f652a776fab24e05', 132, ARRAY ['haas']::data_source[]),
    (7, '55089334dd9c7803537f7351ea6b9a11a77432f9', 77, ARRAY ['smtp']::data_source[]),
    (8, '50f3f01caa053693ce619d596e14b0ff3901ab49', 138, ARRAY ['smtp', 'ftp', 'telnet']::data_source[]),
    (9, '774b2d725a91c5da9e288c87f3162ccb1d3b1361', 28, ARRAY ['haas']::data_source[]),
    (10, '21bd12dc183f740ee76f27b78eb39c8ad972a757', 69, ARRAY ['http']::data_source[]),
    (11, '3090435e9d96ce867fbe90f769083b79744d62ca', 94, ARRAY ['haas']::data_source[]),
    (12, '39c39aafbb766a19c53a1e1038fa68555f33f42a', 11, ARRAY ['smtp']::data_source[]),
    (13, 'e1a47a982f7b7c93e365f3018a55e536e865ee58', 133, ARRAY ['haas']::data_source[]),
    (14, '124448559f477599791f2068f131dbe6c9a4e457', 12, ARRAY ['ftp', 'telnet', 'haas']::data_source[]),
    (15, 'fe2d0a7a5b34951b6ec3c46184f1ed3eae19459d', 72, ARRAY ['haas', 'smtp']::data_source[]),
    (38986, 'd2f4eaea2e7b933b52d3f90a9a7670706389cd58', 92, ARRAY ['haas', 'telnet']::data_source[]),
    (39491, '78ccb27a510d56992b10e40ccd98fcb6743a4be0', 68, ARRAY ['http']::data_source[]),
    (40080, 'f865b53623b121fd34ee5426c792e5c33af8c227', 135, ARRAY ['ftp', 'smtp', 'http']::data_source[]),
    (40499, 'eccb05ebf153a101dee4b59fbcfa9b7a3d6b8bf9', 94, ARRAY ['smtp', 'ftp', 'haas']::data_source[]),
    (40811, '26d8be40f13330a09a4c92cbbbeb3bf1334320b6', 93, ARRAY ['haas']::data_source[]),
    (43626, 'c19f6e601e092bdbee6f1afc41a10fab3b49323c', 35, ARRAY ['http', 'ftp']::data_source[]),
    (46700, '4705593bf39c90a50bc60ea82fb24b9c328116b5', 123, ARRAY ['ftp']::data_source[]),
    (46948, 'fa9beb99e4029ad5a6615399e7bbae21356086b3', 147, ARRAY ['smtp', 'telnet', 'ftp']::data_source[]),
    (47319, 'cab524d4e1c442504f4768ac5a50a2bfb5bcab55', 39, ARRAY ['ftp', 'telnet']::data_source[]),
    (47742, '717f6480311081d89d50b916a2b27a2401393aec', 135, ARRAY ['telnet', 'haas']::data_source[]),
    (54605, '9b9711410589cce0007e091e8345955478d2a78d', 44, ARRAY ['haas']::data_source[]),
    (55755, 'c6ccd9a6e46916d1f8114dc29a7109267cd47574', 24, ARRAY ['smtp', 'ftp']::data_source[]),
    (56522, '9675a920cfe76048e3a9962a35c954a67873d59b', 34, ARRAY ['http', 'smtp']::data_source[]),
    (56558, '7616bb87bd05f6439e3672ba1b2be55d5beb68b3', 93, ARRAY ['telnet']::data_source[]),
    (61170, '6f80dd1bcb87acdcc6f1a344f664fd3499bfae27', 18, ARRAY ['haas', 'http']::data_source[]),
    (62133, '4362a3c32c30891e46e8b17a999d48a790159518', 135, ARRAY ['http']::data_source[]),
    (66062, 'ed3f5e55c038a89450635bcf6d82be255e9ddafb', 77, ARRAY ['telnet']::data_source[]),
    (66185, '9e326a4a7d26fd6f74a12353dd24d4641c717dd3', 96, ARRAY ['haas', 'telnet', 'smtp', 'http', 'ftp']::data_source[]),
    (67179, '006839d264a38b7f58e5c8130447528bf4b7aee1', 1, ARRAY ['haas']::data_source[]),
    (68525, '30a756abd96646694e42165e8b507de6e2ff35a1', 132, ARRAY ['ftp', 'http', 'haas']::data_source[]),
    (71979, '836ef66e1c6619175ae0818ae714a36b5ddb1b4b', 27, ARRAY ['haas']::data_source[]),
    (74184, '5b7d7229fb26cb7cfa62f79c50333a6ba1f8b62e', 65, ARRAY ['haas', 'telnet', 'http', 'smtp', 'ftp']::data_source[]),
    (75602, '6a80667a679382ff315d0c61cdb218145a0511ee', 39, ARRAY ['haas', 'http', 'telnet']::data_source[]),
    (75791, '0e9e8b350faddb98b111a8dc0a81e1d58b3abbf6', 108, ARRAY ['smtp']::data_source[]),
    (97481, '80e22d8b6fc56e9d692cf3c9dba3118e57c1bac2', 43, ARRAY ['smtp']::data_source[]),
    (119674, '0da3f8feec54dc37a6ecd35a1b355f3ba6ef4c00', 124, ARRAY ['http', 'smtp']::data_source[]),
    (133648, 'c8a16b493c487d9f0d43546b842106bf2ffa7152', 30, ARRAY ['http', 'ftp', 'smtp']::data_source[]),
    (134956, '9905c33933602ae804e94f7731ecb5faaf4d6770', 114, ARRAY ['smtp']::data_source[]),
    (148703, '8792476de0c6490027b7dfb0bccdeb6f5b1a6653', 126, ARRAY ['haas']::data_source[]),
    (217660, '6097b3e6c52313f98345c83693bf585f55131ffa', 146, ARRAY ['haas']::data_source[]),
    (218135, 'c95ee47689a0aaec70c3eb950244657722c69b1f', 114, ARRAY ['http']::data_source[]),
    (218244, 'ce7987ef8225cc1a2699a07901f59de7f09bdfed', 129, ARRAY ['http', 'ftp']::data_source[]),
    (224924, '70352f41061eda4ff3c322094af068ba70c3b38b', 85, ARRAY ['ftp', 'http']::data_source[]),
    (228724, '2ea6201a068c5fa0eea5d81a3863321a87f8d533', 89, ARRAY ['ftp', 'http']::data_source[]),
    (228818, 'a1ea31f87ad589e23bc95b4c3f6452f3a3f031eb', 48, ARRAY ['ftp', 'haas']::data_source[]),
    (230372, 'cde189cbec083aaad31d890be94b8a68d463fd7a', 35, ARRAY ['ftp', 'haas', 'http', 'smtp']::data_source[]),
    (231532, 'c177922cb7715a94aa4758eb140e08bfce4c5a04', 73, ARRAY ['ftp']::data_source[]),
    (233526, 'eeac0f0e950a0bb7a75f35275352bffcb94ecdd6', 89, ARRAY ['ftp']::data_source[]),
    (234012, '5c52cbc07e40a5b8dfb43817803cbb4f32932afc', 126, ARRAY ['ftp']::data_source[]),
    (234718, 'fcd4cc078aa4809083206f96cb697725cc0d443a', 106, ARRAY ['haas', 'ftp']::data_source[]),
    (235791, '630db2cecb0e0eaa26825a094b6d63b830d92fd0', 144, ARRAY ['http', 'ftp', 'telnet']::data_source[]),
    (237042, '404865caadc10463069501335969936e4fa9d48d', 134, ARRAY ['smtp', 'telnet']::data_source[]),
    (239345, '7b005f48d13e6ffdd4ca9ffc1711827173993cc0', 32, ARRAY ['http', 'telnet', 'haas', 'smtp']::data_source[]),
    (240606, '7b902e6ff1db9f560443f2048974fd7d386975b0', 76, ARRAY ['ftp']::data_source[]),
    (240988, '0f4d09e43d208d5e9222322fbc7091ceea1a78c3', 55, ARRAY ['http']::data_source[]),
    (242680, 'a9440e0bbd7e313da632dc843afb223884a30bfe', 26, ARRAY ['smtp', 'ftp', 'haas']::data_source[]),
    (242841, '5d83d5b654d228c3bd02a5d83892bb01825848bc', 111, ARRAY ['ftp', 'http']::data_source[]),
    (243656, '82a1d56b7f875573b11a150ae703e08ee3f9bcf3', 108, ARRAY ['ftp', 'http']::data_source[]),
    (244577, 'b667bad5682615235dc88e64dcbaaefae8958e99', 33, ARRAY ['haas', 'ftp', 'smtp', 'telnet']::data_source[]),
    (245520, '4b9bfe79c9d63dbe77c290a0cd59f2a729186c1e', 39, ARRAY ['ftp']::data_source[]),
    (246143, '4cf5bc59bee9e1c44c6254b5f84e7f066bd8e5fe', 22, ARRAY ['http']::data_source[]),
    (253171, 'b82dd601409bba5818c9142e3a29774f650ca0ad', 52, ARRAY ['telnet']::data_source[]),
    (256315, 'ae31347c922446d1f855c0da0fccc493800515d8', 10, ARRAY ['haas', 'telnet', 'http', 'smtp', 'ftp']::data_source[]),
    (258824, 'd32ff024758f291dc0dcd49a0b41e01834c5c2ab', 92, ARRAY ['http']::data_source[]),
    (260261, 'bdb985a5b9b4202d8ea6be8189f4b6f15179bf18', 50, ARRAY ['haas']::data_source[]),
    (260983, 'cf21d8584300263ad59d8153217c2fe3e87ff2fd', 147, ARRAY ['haas', 'telnet']::data_source[]),
    (261876, '3f9f1dae9b6f6674351850ba70ba53eee4154d6f', 143, ARRAY ['smtp', 'http']::data_source[]),
    (263437, '94f2272c586f7d9c5de438a8d8045764e2a32ceb', 52, ARRAY ['ftp']::data_source[]),
    (264580, '34b6ede1308f851b7cfc07acc36a8abff2fc3b1c', 20, ARRAY ['haas']::data_source[]),
    (265850, '1b10fe8c1f2f5c29f78faafa526afd210ded9fb2', 111, ARRAY ['smtp', 'ftp', 'haas', 'telnet', 'http']::data_source[]),
    (268535, '67bc002403c6398d97449c3cdc66960b733d7c95', 53, ARRAY ['smtp', 'telnet']::data_source[]),
    (270838, '6db69219ec7196726d520f76f190f6550ad35543', 1, ARRAY ['haas']::data_source[]),
    (271013, '957b77b65a6526c830b17799cf87e639ef6c230f', 27, ARRAY ['http', 'haas', 'smtp']::data_source[]),
    (274403, '7b9f28a26a49353923a161bf1b848900ea59f1e9', 145, ARRAY ['ftp', 'smtp']::data_source[]),
    (275867, '1d0384de54c85efb3dcc3c254e12a60e9ac864ae', 16, ARRAY ['ftp']::data_source[]),
    (281642, 'ddfdc957b3145c014c7b8561c511182a25ffbd24', 77, ARRAY ['haas']::data_source[]),
    (282973, 'b68d7724bb92389efb202942acba20a2850d8e53', 72, ARRAY ['smtp', 'http', 'ftp']::data_source[]),
    (288272, '90d3cf824884e6579cb9aff79fc70b752be04c6d', 27, ARRAY ['haas']::data_source[]),
    (291694, '20cda97d9c379b55577da789f2435a3ab060e48d', 19, ARRAY ['telnet']::data_source[]),
    (303071, 'b5e701c92eb74de4d60cdc06f349e4cf009dad65', 78, ARRAY ['smtp', 'haas']::data_source[]),
    (304158, '97b5b32ef1c85e74647ab3f87f45c5d23053a4da', 62, ARRAY ['ftp', 'haas']::data_source[]),
    (314110, '3593b8021e5b563dc8cb9750e889ba3a9f4d02cc', 114, ARRAY ['haas', 'telnet', 'ftp', 'smtp']::data_source[]),
    (315742, 'b0faceaa18147d777fb9562fd86aff6b3091c1f7', 119, ARRAY ['http']::data_source[]),
    (315748, '72fee33909f033b2ce00424683c9fc78af860f5a', 12, ARRAY ['haas', 'http']::data_source[]),
    (317376, '35675e68f4b5af7b995d9205ad0fc43842f16450', 80, ARRAY ['smtp', 'http', 'haas', 'telnet', 'ftp']::data_source[]),
    (328597, '068767b389590dbb57dd3c5b7bc66971afcdf17d', 68, ARRAY ['telnet']::data_source[]),
    (352435, '65dd0fb09a34055a8e1be4d29535314c7e41b2f0', 66, ARRAY ['ftp', 'telnet']::data_source[]),
    (366564, '5bdcd3c0d4d24ae3e71b3b452a024c6324c7e4bb', 146, ARRAY ['haas']::data_source[]),
    (371728, '8df2ae0668218b74822da6e7de4d18b678230bd6', 16, ARRAY ['ftp']::data_source[]),
    (382543, '162aab82f860eee1616d5b1a3e83eee3956710b2', 52, ARRAY ['ftp', 'smtp', 'http']::data_source[]),
    (384091, '84e28d61e017bd7f37637e1f2581b1bcb3385cf3', 142, ARRAY ['haas']::data_source[]),
    (456523, '6401561d8326540f8d1be2112081432d8ddf62da', 101, ARRAY ['http', 'ftp', 'smtp']::data_source[]),
    (465671, '9d4e1e23bd5b727046a9e3b4b7db57bd8d6ee684', 10, ARRAY ['ftp', 'telnet']::data_source[]),
    (472686, '1411678a0b9e25ee2f7c8b2f7ac92b6a74b3f9c5', 111, ARRAY ['ftp', 'http', 'telnet']::data_source[]),
    (484606, '011c945f30ce2cbafc452f39840f025693339c42', 22, ARRAY ['http', 'ftp']::data_source[]),
    (505648, '180a4def3cfd00b29905c73a437ced125211f233', 133, ARRAY ['ftp', 'telnet']::data_source[]),
    (508844, '74913f5cd5f61ec0bcfdb775414c2fb3d161b620', 103, ARRAY ['http', 'telnet', 'haas', 'ftp', 'smtp']::data_source[]),
    (530865, 'b379600422e3069166ff59d8d0871c61f5388b43', 67, ARRAY ['ftp', 'haas']::data_source[]),
    (547188, '348162101fc6f7e624681b7400b085eeac6df7bd', 94, ARRAY ['http']::data_source[]),
    (557319, '12dea96fec20593566ab75692c9949596833adc9', 66, ARRAY ['haas']::data_source[]),
    (572797, '1f82c942befda29b6ed487a51da199f78fce7f05', 78, ARRAY ['ftp', 'haas']::data_source[]),
    (582713, '7c4a8d09ca3762af61e59520943dc26494f8941b', 138, ARRAY ['smtp']::data_source[]),
    (691747, 'dc76e9f0c0006e8f919e0c515c66dbba3982f785', 25, ARRAY ['smtp']::data_source[]),
    (720788, '7505d64a54e061b7acd54ccd58b49dc43500b635', 36, ARRAY ['http']::data_source[]),
    (752398, '5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', 55, ARRAY ['smtp', 'ftp']::data_source[]),
    (1000068, '7110eda4d09e062aa5e4a390b0a572ac0d2c0220', 2, ARRAY ['smtp', 'telnet']::data_source[]),
    (1086740, 'd033e22ae348aeb5660fc2140aec35850c4da997', 68, ARRAY ['haas', 'telnet']::data_source[]),
    (1123319, '8cb2237d0679ca88db6464eac60da96345513964', 101, ARRAY ['http']::data_source[]),
    (1384875, 'ec122f54cf16a175b3e22979e240684f7734079a', 68, ARRAY ['ftp', 'smtp', 'telnet']::data_source[]),
    (1620212, '317f1e761f2faa8da781a4762b9dcc2c5cad209a', 93, ARRAY ['smtp', 'telnet']::data_source[]);