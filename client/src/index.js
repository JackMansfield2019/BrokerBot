import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import AppRouter from './AppRouter';
import reduxStore from './redux/store'
import './style.css';

//Need to add the redux store in Provider Tag
ReactDOM.render(
  <Provider store={reduxStore}>
    <AppRouter />
  </Provider>,
  document.getElementById('root')
);