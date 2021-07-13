import React from 'react';
import { BrowserRouter, Switch } from 'react-router-dom';

import PrivateRoute from './Components/Routes/PrivateRoute';
import PublicRoute from './Components/Routes/PublicRoute';

/*------------------------------ App Pages ------------------------------*/
import LoginPage from './Components/Pages/LoginPage/index';
import HomePage from './Components/Pages/HomePage/index';



class AppRouter extends React.Component {
  render() {
    return (
      <BrowserRouter>
          <Switch> 
            {/*  ------------------  Public Routes Below ------------------- */}
            <PublicRoute component={LoginPage} path={'/'} exact />
            {/*  ------------------  Private Routes Below ------------------ */}
            <PrivateRoute component={HomePage} path={'/Home'} exact />
          </Switch>
      </BrowserRouter>
    );
  }
}

export default AppRouter;