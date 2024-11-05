import Home from "./pages/Home";
import {Route,Routes }from 'react-router-dom';
import Login from "./pages/Login";
import Signup from "./pages/signup";
import Navbar from "./components/Navbar"

function App(){
  return (
    <div className='min-h-screen bg-gray-900 text-white relative overflow-hidden'> 
     <div className='absolute inset-0 overflow-hidden'>
      <div className='absolute inset-0'>
        <div className='absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(ellipse_at_top, rgba(16,185,129,0.3)_0%, rgba(10,80,60,0.2)_45%,rgba(0,0,0,0.1)_100%)]' />
      </div>
     </div>
     <div className>
     <Navbar/>

      <Routes>
        <Route path='/' element={ <Home/>}/>
        <Route path='/Signup' element={ <Signup/>}/>
        <Route path='/Login' element={ <Login/>}/>

      </Routes>
      </div>
    </div>
  )

}
export default App;