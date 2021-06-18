import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';


// Use ES6 object literal shorthand syntax to define the object shape
export default configureStore({
  reducer: {
    userData: userReducer,
  }
})
