import React from 'react';
import { MdInfo } from "react-icons/md";

class SummaryDisplay extends React.Component {

    constructor(props){
    super(props); 

        this.state = {
            /*Fill in the state variables later with Broker Data needed for graphs and bots */
        }
    }


  render() {
    return  <div className="summary-display-wrapper" >
                <div className="data-display-header" >
                    <div className="data-display-header-first" >
                        <div className="data-display-title-wrapper">
                            {this.props.title}
                        </div>
                    </div>
                    {this.props.categories.map((categoryName) => {
                      return <div className="data-display-header-category">{categoryName}</div>
                    })}
                     <div className="data-display-cell-last" />
                </div>
                <div className="data-display-content" >
                    {this.props.inputData.map((data) =>{
                        return  <><div className="data-display-cell" >
                                    <div className="data-display-cell-first" >
                                        <div className="data-display-title-wrapper">{data.title}</div>
                                    </div>
                                    {data.values.map((categoryValues) => {
                                        return <div className="data-display-cell-content" >{categoryValues}</div>
                                    })}
                                         <div className="data-display-cell-last" style={{color: "#24a0ed"}} >  <MdInfo size={18} /></div>
                                    </div>  
                                    <div class="divider">
                                 </div>
                                </>
                            
                    })} 
                </div>
            </div>
  }
}

export default SummaryDisplay;