let e = require('datatables.net-editor-server');
 
let Editor = e.Editor;
let Field = e.Field;
let Validate = e.Validate;
let Format = e.Format;

let knex = require('knex');
 
module.exports = knex({
    client: 'mysql',
 
    connection: {
        database:    'stateline_tools_db',
        host:        'localhost',
        password:    'roothost1',
        user:        'root',
        dateStrings: true
    }
});