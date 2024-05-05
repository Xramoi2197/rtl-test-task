// Импорт необходимых модулей
const fs = require('fs');
const path = require('path');

const username = process.env.MONGO_INITDB_ROOT_USERNAME;
const password = process.env.MONGO_INITDB_ROOT_PASSWORD;
const uri = `mongodb://${username}:${password}@localhost:27017/`;
print(uri)
// Установка соединения с MongoDB
const conn = new Mongo(uri);
const db = conn.getDB("sampleDB");

// Путь к дампу
const dumpDir = '/usr/src/app/dump/sampleDB';

// Имя коллекции
const collectionName = 'sample_collection';

// Путь к файлам дампа
const metadataPath = path.join(dumpDir, collectionName + '.metadata.json');
const bsonPath = path.join(dumpDir, collectionName + '.bson');

// Проверка наличия файлов
if (!fs.existsSync(metadataPath) || !fs.existsSync(bsonPath)) {
    print('Error: Metadata or BSON file not found');
    quit(1);
}

// Создание коллекции
db.createCollection(collectionName);

// Импорт метаданных коллекции
const metadata = JSON.parse(cat(metadataPath));
const options = { collation: metadata.options.collation };
db[collectionName].createIndexes(metadata.indexes, options);

// Импорт данных из BSON файла
const bsonData = bsonWoHelper.load(bsonPath);
const bsonArray = bsonData.toArray();

db[collectionName].insertMany(bsonArray);