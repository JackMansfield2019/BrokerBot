import React from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
import { connect } from 'react-redux';
//import { ROUTES } from '/routes';

function PrivateRoute(props: RouteProps): React.ReactElement {
    const { component: Component, ...rest } = props;

    const render = props => {
        if (!props.isAuthenticated && false) {
            return <Redirect to={'/'} />;
        }

        return <Component {...props} />;
    };

    return <Route {...rest} render={render} />;
}

const MapStateToProps = (state) => ({
    isAuthenticated: state.userData.isAuthenticated
});

export default connect(MapStateToProps)(PrivateRoute);