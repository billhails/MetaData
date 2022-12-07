BEGIN TRANSACTION;
INSERT INTO "categories" VALUES ('75588ab7-2ea1-49fb-ad52-7a79a3165ebf','Philosophy'),
 ('889bbd27-2567-404a-ad8f-618d30286967','Science'),
 ('d5c594a5-5c15-42a8-8ccf-c5eb3baa7664','Art');
INSERT INTO "roles" VALUES ('c626306e-b092-4aed-ad66-3521b25654f1','admin');
INSERT INTO "users" VALUES ('401fed0d-3c59-4ea1-bd7d-fc4acc4d2da2','bill','me@example.com','$2b$10$AQMez1dNfRW5BmVUF.BRfeMG3/cHFvH28T5muZkdcylrfo4vWjDnK');
INSERT INTO "refresh_tokens" VALUES ('ce76e5ed-c6c6-4a3a-a01d-571f7280953b','eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Im1lQGV4YW1wbGUuY29tIiwic3ViIjoiNDAxZmVkMGQtM2M1OS00ZWExLWJkN2QtZmM0YWNjNGQyZGEyIiwiaWF0IjoxNjcwNDMzNjYzfQ.6mMDm4xKAHJA2Hj4Mczpgw5O2Y34m-iYDl1ojcOXDvM','401fed0d-3c59-4ea1-bd7d-fc4acc4d2da2');
INSERT INTO "users_roles" VALUES ('401fed0d-3c59-4ea1-bd7d-fc4acc4d2da2','c626306e-b092-4aed-ad66-3521b25654f1');
COMMIT;
