const bfj = require('bfj');
const { MongoClient} = require("mongodb");


const lowercaseKeys = obj =>
  Object.keys(obj).reduce((acc, key) => {
    acc[key.toLowerCase()] = obj[key];
    return acc;
  }, {});



bfj.read("../districts.geojson" )
  .then(async data => {
    try{
        const client = new MongoClient("mongodb://localhost:27017/rethink");
        await client.connect()
        const database = await client.db('rethink');
        const collection = await database.collection('districts');
        await collection.createIndex({ 'geometry' : "2dsphere" })
        for(let feature of data["features"]){
            transformed = lowercaseKeys(feature["properties"])
            transformed["geometry"] = feature['geometry']
            console.log(feature["geometry"]["coordinates"][1])
            // await collection.insertOne(transformed)
            console.log("collection inserted")
        }
       

    }catch(e){
        console.log(e)
    }
  })
  .catch(error => {
      console.log(error)
    // :(
  });
