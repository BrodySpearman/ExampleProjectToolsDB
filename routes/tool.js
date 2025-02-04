let db = require('./node_scripts/db');
let router = require('express').Router();
let {
    Editor,
    Field,
    Validate,
    Format,
    Options
} = require('datatables.net-editor-server');
 
router.all('/api/tool', async function(req, res) {
    let editor = new Editor( db, 'Tool', 'ToolID' )
        .fields(
            new Field( 'ToolID' ),
            new Field( 'Type' ),
            new Field( 'ToolName' ),
            new Field( 'Brand' ),
            new Field( 'SKU' ),
            new Field( 'SerialNum' ),
            new Field( 'Description' )
        );
 
    await editor.process(req.body);
    res.json( editor.data() );
} );

module.exports = router;