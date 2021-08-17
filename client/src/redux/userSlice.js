import { createAsyncThunk , createSlice } from '@reduxjs/toolkit';

/*
export const veryifyLogin = createAsyncThunk(
    'user/auth/veryifyLogin',
    async(payload) => {
       const response = await fetch('http://localhost:8000/user/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ taskData: payload }),
        });

        if( response.ok ){
            const resp = await response.json();
            return  resp ;
        } 
    }  
);

export const verifyRegister = createAsyncThunk(
    'user/auth/veryifyRegister',
    async(payload) => {
       const response = await fetch('http://localhost:8000/user/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ taskData: payload }),
        });

        if( response.ok ){
            const resp = await response.json();
            return  resp ;
        } 
    }  
);
*/
export const userSlice = createSlice({
    name: 'userData',
    initialState: {
        userID: '',
        userEmail: '',
        isAuthenticated: false, 
        isRegister: false,
    },
    reducers: {
        userLogin: (state, actions) => {
            state.userEmail = actions.payload.email;
            state.userID = actions.payload.ID;
            state.isAuthenticated = true;
            state.isRegister = false;
        },
        userRegister: (state, actions) => {
            state.userEmail = actions.payload.email;
            state.userID = actions.payload.ID;
            state.isAuthenticated = true;
            state.isRegister = true;
        }
    },
    /*extraReducers: {
    [verifyLogin.fulfilled]: (state, action) => {
        //update the state based on response
    },
    [verifyResponse.fulfilled]: (state, action) => {
        //update the state based on the response
    }, */


});


export const { userLogin, userRegister } = userSlice.actions;
export default userSlice.reducer;
