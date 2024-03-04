import './App.css';
import Login from './components/login'
import CreateUser from './components/CreatUser';
import Forgot from './components/Forgot';
import Dashboard from './components/Dashboard';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import React from 'react';
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
              <Route path="/" element={<Login />}>
                  {/*<Route path="projects" element={<Projects />} />*/}
                  {/*/!*{ <Route path="*" element={<NoPage />} />}*!/*/}
              </Route>
              <Route path="/Create-User" element={<CreateUser />}>
                  {/*<Route path="projects" element={<Projects />} />*/}
                  {/*/!*{ <Route path="*" element={<NoPage />} />}*!/*/}
              </Route>
              <Route path="/Forgot" element={<Forgot />}>
                  {/*<Route path="projects" element={<Projects />} />*/}
                  {/*/!*{ <Route path="*" element={<NoPage />} />}*!/*/}
              </Route>
              <Route path="/Dashboard" element={<Dashboard />}>
                  {/*<Route path="projects" element={<Projects />} />*/}
                  {/*/!*{ <Route path="*" element={<NoPage />} />}*!/*/}
              </Route>
          </Routes>
      </BrowserRouter>
  );
}

export default App;
