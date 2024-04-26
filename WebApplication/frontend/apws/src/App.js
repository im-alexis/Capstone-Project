import "./App.css";
import Login from "./components/login";
import Landing from "./components/landing";
import CreateUser from "./components/CreateUser";
import Forgot from "./components/Forgot";
import Dashboard from "./components/Dashboard";
import Register from "./components/Register";
import NotFound from "./components/errorPage";
import Join from "./components/join";
import History from "./components/History";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import React from "react";
import Verify from "./components/verify";
import Reset_password from "./components/reset_password";
import Plant_Settings from "./components/settings";
// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />}></Route>
        <Route path="/Login" element={<Login />}></Route>
        <Route path="/Create-User" element={<CreateUser />}></Route>
        <Route path="/Forgot" element={<Forgot />}></Route>
        <Route path="/Dashboard" element={<Dashboard />}></Route>
        <Route path="/verify" element={<Verify />}></Route>
        <Route path="/reset_password" element={<Reset_password />}></Route>
        <Route path="/Register" element={<Register />}></Route>
        <Route path="/Join" element={<Join />}></Route>
        <Route path="/Plant_Settings" element={<Plant_Settings />}></Route>
        <Route path="/plantHistory" element={<History />}></Route>
        <Route path="*" element={<NotFound />}>
          {/*<Route path="projects" element={<Projects />} />*/}
          {/*/!*{ <Route path="*" element={<NoPage />} />}*!/*/}
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
