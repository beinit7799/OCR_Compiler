const express = require("express");
const app = express();
var cors = require("cors");

var compiler = require("compilex");
var options = { stats: true }; //prints stats on console
compiler.init(options);
// app.use(bodyParser);
app.use(cors());
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post("/run", (req, res) => {
  const { code } = req.body;
  try {
    // if ((lang = "cpp")) {
    // if (!input) {
    var envData = { OS: "windows", cmd: "g++" }; // (uses g++ command to compile )
    //var envData = { OS: "linux", cmd: "gcc" }; // ( uses gcc command to compile ) FOR LINUX
    compiler.compileCPP(envData, code, function (data) {
      // if (data.output) {
      //   res.send(data);
      // } else {
      //   res.send({ output: "error" });
      // }
      res.send(data);
      console.log("INSIDE");
    });
    // } else {
    //   var envData = { OS: "windows", cmd: "g++" }; // (uses g++ command to compile )
    //   // var envData = { OS: "linux", cmd: "gcc" }; // ( uses gcc command to compile ) FOR LINUX
    //   compiler.compileCPPWithInput(envData, code, input, function (data) {
    //     if (data.output) {
    //       res.send(data);
    //     } else {
    //       res.send({ output: "error" });
    //     }
    //   });
    // }
    // }
  } catch (e) {
    console.log(e);
  }
});

app.post("/test", (req, res) => {
  const { code } = req.body;
  var envData = { OS: "windows", cmd: "g++" };
  compiler.compileCPP(envData, code, function (data) {
    res.send(data);
  });
});

app.post("/py", (req, res) => {
  const { code, input } = req.body;
  var envData = { OS: "windows" };
  // compiler.compilePython(envData, code, function (data) {
  //   res.send(data);
  // });
  compiler.compilePythonWithInput(envData, code, input, function (data) {
    res.send(data);
  });
});

// app.post("/py", (req, res) => {
//   const { code } = req.body;
//   var envData = { OS: "windows" };
//   const rl = readline.createInterface({
//     input: process.stdin,
//     output: process.stdout
//   });
//   rl.question('Enter input: ', (input) => {
//     compiler.compilePythonWithInput(envData, code, input, function (data) {
//       res.send(data);
//       rl.close();
//     });
//   });
// });

app.post("/cpp", (req, res) => {
  const { code } = req.body;
  var envData = { OS: "windows", cmd: "g++" };
  compiler.compileCPP(envData, code, function (data) {
    res.send(data);
  });
});

app.listen(4999, () => {
  console.log(`Listening on port 4999!`);
});
