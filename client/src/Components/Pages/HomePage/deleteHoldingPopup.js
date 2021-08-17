import React from 'react';

class DeleteHoldingPopup extends React.Component  {

     constructor(props){
        super(props); 

        this.state = {
           
        }
    }

    
    /**
     * This function changes the display value of the add calendar pop up menu.
     *
     * @param   {boolean} value A boolean true or false
     * @effect  Changes deleteHoldingPopup: value to be the input value and if the boolean is true it sets the delete Holding pop up to 
     *          be displayed on the screen, Otherwise if it is false it will not diplay the add to calendar pop up on the screen.
     */
    YesBtnPressed = () => {
        this.props.setTrigger(false);
        this.props.delHold(this.props.holdingName);
    }

    /**
     * This function is the response for no being presseed in delete holding popup
     *
     * @effect  Cancels the request to delete the task and sends User back to the dashboard
     */
    NoBtnPressed = () => {
        this.props.setTrigger(false);
    }

    render(){
        return  <div className="del-hold-popup-inner">
                    <div className="del-hold-title" >Delete Holding</div>
                    <div className="del-hold-popup-content" >Are you sure you want to delete the holding {this.props.holdingName} , this action is can not be undone.</div>
                    <div className="del-hold-popup-button-wrapper" >
                        <div className="del-hold-popup-button-left"  >
                           <button onClick={() => this.YesBtnPressed()} /> Yes
                        </div>
                        <div className="del-hold-popup-button-right" >
                              <button onClick={() => this.NoBtnPressed()} /> No
                        </div>
                    </div>
                </div>
    }
}

export default DeleteHoldingPopup;