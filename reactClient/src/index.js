import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter} from 'react-router-dom';
import './index.css';
import SearchPage from './Components/searchComponents/SearchPage';
import * as serviceWorker from './Components/searchComponents/serviceWorker';



ReactDOM.render((<BrowserRouter> <SearchPage/> </BrowserRouter>), document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();