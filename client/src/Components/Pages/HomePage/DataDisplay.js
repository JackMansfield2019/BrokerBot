import React from 'react';
import { MdDeleteForever, MdAddCircle } from "react-icons/md";


let key = 1;
class DataDisplay extends React.Component {

    constructor(props){
    super(props); 

        this.state = {
          
        }
    }

    testing = () => {
        console.log("IM SO DONE WITH THIS")
    }
  render() {
    return  <div className="data-display-wrapper" >
                <div className="data-display-header" >
                    <div className="data-display-header-first" >
                        <div className="data-display-title-wrapper">
                            {this.props.title}
                        </div>
                    </div>
                    {this.props.categories.map((categoryName) => {
                      return <div className="data-display-header-category">{categoryName}</div>
                    })}
                       <div className="data-display-cell-last" ></div>    
                </div>
                <div className="data-display-content" >
                    {this.props.inputData.map((data, index, arr) =>{
                        
                        return  index === arr.length -1 ? 
                                  <><div className="data-display-cell" >
                                        <div className="data-display-cell-first" key={key++} >
                                            <div className="data-display-title-wrapper" key={key++}>{data.title}</div>
                                        </div>
                                        {data.values.map((categoryValues) => {
                                            return <div className="data-display-cell-content" key={key++} >{categoryValues}</div>
                                        })}
                                          <div className="data-display-cell-last" key={key++}  >
                                                  <button type="button" rkey={key++} onClick={() => this.props.delPopupTrigger(true, data.title)} />
                                            <MdDeleteForever size={20} />
                                          </div>    
                                    </div></> : 
                                  <><div className="data-display-cell" key={key++} >
                                        <div className="data-display-cell-first" key={key++} >
                                            <div className="data-display-title-wrapper" key={key++}>{data.title}</div>
                                        </div>
                                        {data.values.map((categoryValues) => {
                                            return <div className="data-display-cell-content" key={key++} >{categoryValues}</div>
                                        })}
                                          <div className="data-display-cell-last" key={key++}   >
                                            <button type="button" rkey={key++} onClick={() => this.props.delPopupTrigger(true, data.title)} />
                                            <MdDeleteForever size={20} />
                                        
                                          </div>    
                                    </div><div class="divider" key={key++}/>
                                  </>     
                    })} 
                </div>
                <div className="data-display-footer" >
                    <div className="data-display-cell" >
                        <div className="data-display-cell-first" >
                            <div className="data-display-title-wrapper">{"Grand Total (USD) Since Jul. 24 2021 "}</div>
                        </div>
                        {this.props.resultValues.map((categoryValues) => {
                            return <div className="data-display-cell-content" >{categoryValues}</div>
                        })}
                        <div className="data-display-cell-last" style={{color: "#77DD77"}} >
                                 <button type="button" rkey={key++} onClick={() => this.props.addPopupTrigger(true)} />
                        <MdAddCircle size={20} />
                        </div> 
                    </div>  
                </div>

            </div>
  }
}

export default DataDisplay;