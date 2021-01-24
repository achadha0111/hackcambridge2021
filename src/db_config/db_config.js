import tedious from 'tedious';

const config = {
    authentication: {
        options: {
            userName: process.env.db_username,
            password: process.env.db_password
        },
        type: "default"
    },
    server: process.env.db_server, // update me
    options: {
        database: "votingDB", //update me
        encrypt: true
    }
};

const connection = new tedious.Connection(config);

export default connection;