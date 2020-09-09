var spawn = require('child_process').spawn;

// var run_lib = spawn('python3', ['./lib_sparrow_lte.exe']);

// run_lib.stdout.on('data', function(data) {
//     console.log('stdout: ' + data);
// });

// run_lib.stderr.on('data', function(data) {
//     console.log('stderr: ' + data);
// });

// run_lib.on('exit', function(code) {
//     console.log('exit: ' + code);
// });

// run_lib.on('error', function(code) {
//     console.log('error: ' + code);
// });

const { execFile } = require('child_process');
const child = execFile('./lib_sparrow_lte.exe', ['/dev/ttyUSB1', '115200'], (error, stdout, stderr) => {
  if (error) {
    throw error;
  }
  console.log(stdout);
});