import { createSlice } from '@reduxjs/toolkit';

export const userSlice = createSlice({
    name: 'userData',
    initialState: {
        userID: '',
        userEmail: '',
        isAuthenticated: false, 
    },
    reducers: {
        userLogin: (state, actions) => {
            state.userEmail = actions.payload.email;
            state.userID = actions.payload.ID;
            state.isAuthenticated = true;
        }
    }


});


export const { userLogin } = userSlice.actions;
export default userSlice.reducer;