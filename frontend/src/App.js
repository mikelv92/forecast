import React, { Component } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { TextField, Grid, Card, CardContent, Typography } from '@material-ui/core';

const axios = require('axios');
const moment = require('moment');

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            uga_data: [],
            corn_data: [],
            ndaq_data: [],
            months: 1,
            predictions: {
                CORN: {
                    mean: 0
                },
                UGA: {
                    mean: 0
                },
                NDAQ: {
                    mean: 0
                }
            }
        }
    }

    getData(months = 1) {
        axios
            .get('/data?data_type=uga&months=' + months)
            .then(results => {
                return results.data.map((d) => {
                    return { date: d.Date, value: d.Close }
                });
            })
            .then((data) => {
                this.setState({ uga_data: data });
            });

        axios
            .get('/data?data_type=corn&months=' + months)
            .then(results => {
                return results.data.map((d) => {
                    return { date: d.Date, value: d.Close }
                });
            })
            .then(data => {
                this.setState({ corn_data: data })
            });

        axios
            .get('/data?data_type=ndaq&months=' + months)
            .then(results => {
                return results.data.map((d) => {
                    return { date: d.Date, value: d.Close }
                });
            })
            .then(data => {
                this.setState({ ndaq_data: data })
            });

        axios
            .get('/predict')
            .then(results => {
                console.log(results.data);
                this.setState({ predictions: results.data })
            });

        this.setState({ months: months })
    }

    componentWillMount() {
        this.getData();
    }

    handleChange(event) {
        if (event.target.value)
            this.getData(event.target.value)
    }

    render() {
        const uga_data = this.state.uga_data;
        const corn_data = this.state.corn_data;
        const ndaq_data = this.state.ndaq_data;

        const lastMonthDate = moment().subtract(this.state.months, 'months');
        const duration = Math.round(moment.duration(moment().diff(lastMonthDate)).asDays());

        let data = Array.from(Array(duration), (e, i) => {
            const ugaCurrent = uga_data.find(x => x.date === moment().subtract(i, 'days').format('YYYY-MM-DD'));
            const cornCurrent = corn_data.find(x => x.date === moment().subtract(i, 'days').format('YYYY-MM-DD'));
            const ndaqCurrent = ndaq_data.find(x => x.date === moment().subtract(i, 'days').format('YYYY-MM-DD'));

            const ugaValue = ugaCurrent ? ugaCurrent.value : null;
            const cornValue = cornCurrent ? cornCurrent.value : null;
            const ndaqValue = ndaqCurrent ? ndaqCurrent.value : null;

            return {
                date: moment().subtract(i, 'days').format('YYYY-MM-DD'),
                UGA: ugaValue,
                CORN: cornValue,
                NDAQ: ndaqValue
            }
        });

        data = data.reduce((acc, cur) => {
            if (cur.UGA || cur.CORN || cur.NDAQ) acc.push(cur);
            return acc;
        }, []);

        data = data.sort((a, b) => a.date < b.date ? -1 : 1);

        return (
            <Grid container style={{ flexGrow: 1, marginTop: 30 }} spacing={24} direction='row' justify='center' alignItems='center'>
                <Grid item xs={9} style={{ marginLeft: 90 }}>
                    <Chart data={data} />
                </Grid>
                <Grid item xs={3}>
                    <TextField defaultValue={1} label={'Months'} variant='outlined' onChange={(e) => this.handleChange(e)}></TextField>
                </Grid>
                <Grid item xs={3}>
                    <Card>
                        <CardContent>
                            <Typography>
                                Prediction
                            </Typography>
                            <Typography>
                                UGA: {Math.round(this.state.predictions.UGA.mean * 100) / 100}
                            </Typography>
                            <Typography>
                                CORN: {Math.round(this.state.predictions.CORN.mean * 100) / 100}
                            </Typography>
                            <Typography>
                                NDAQ: {Math.round(this.state.predictions.NDAQ.mean * 100) / 100}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        );
    }
}

class Chart extends React.Component {
    render() {
        return (
            <LineChart width={1000} height={300} data={this.props.data}
                margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="UGA" stroke="#8884d8" />
                <Line type="monotone" dataKey="CORN" stroke="#1884d8" />
                <Line type="monotone" dataKey="NDAQ" stroke="#088428" />
            </LineChart>
        );
    }
}

export default App;
