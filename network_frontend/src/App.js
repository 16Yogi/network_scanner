import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './Layout/Layout';
import Scan from './Component/Scan/Scan';
import Registration from './Component/Registration/Registration';
import Login from './Component/Registration/Login';
import Logout from './Component/Registration/Logout';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Layout />}>
          <Route index element={<Scan />} />       
          <Route path='scan' element={<Scan />} /> 
          <Route path='registration' element={<Registration/>}/>
          <Route path='login' element={<Login/>}/>
          <Route path='logout' element={<Logout/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
