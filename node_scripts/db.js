let knex = require('knex');
 
module.exports = knex({
    client: 'mysql',
 
    connection: {
        database:    'stateline_tools_db',
        host:        'localhost',
        password:    'roothost1',
        user:        'root',
        dateStrings: true,
        port: 3000
    }
});