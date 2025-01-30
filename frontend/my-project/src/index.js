import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import App from './App';
import Signup from './components/Signup';
import Login from './components/Login';
import Survey from './components/Survey';
import Main from './components/Main';
import Swot from './components/Swot'
import Sense from './components/Sense';
import Sense_List from './components/Sense_List';
import Sense_Result from './components/Sense_Result';
import Swot_Performance from './components/Swot_Performance';
import Swot_Engagement from './components/Swot_Engagement'
import Swot_Revenue from './components/Swot_Revenue'
import { GoogleOAuthProvider } from '@react-oauth/google';

ReactDOM.createRoot(document.getElementById('root')).render(
  <GoogleOAuthProvider clientId="48244054796-8217g0gh724otkh1sl8r3fp7dfu0l5b8.apps.googleusercontent.com">
    <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/survey" element={<Survey />} />
        <Route path="/main" element={<Main />} />
        <Route path="/main/sense" element={<Sense />} />
        <Route path="/main/senselist" element={<Sense_List />} />
        <Route path="/main/sense/:id" element={<Sense_Result />} />
        <Route path='/main/Swot' element={<Swot/>}/>
        <Route path="/main/Swot/Performance" element={<Swot_Performance />} />
        <Route path="/main/Swot/Engagement" element={<Swot_Engagement />} />
        <Route path="/main/Swot/Revenue" element={<Swot_Revenue />} />
      </Routes>
    </Router>
  </GoogleOAuthProvider>
);