import React from 'react'


export default function Popup(props) {
    return (props.trigger) ? (
        <div className="popup"  >
            { props.children }
        </div>
    ) : <></>;
}