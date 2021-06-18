import React from 'react';
import { Route, Redirect, RouteProps } from 'react-router-dom';
//import { ROUTES } from '../constants';

interface PublicRouteProps {
    restricted?: boolean;
}

function PublicRoute(props: PublicRouteProps & RouteProps): React.ReactElement {
    const { component: Component, restricted = false, ...rest } = props;

    const render = props => {
        if ( restricted ) {
            return <Redirect to={'/'} />;
        }

        return <Component {...props} />;
    };

    return <Route {...rest} render={render} />;
}

export default PublicRoute;