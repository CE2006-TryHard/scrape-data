const csv = require('csv-parser')
const fs = require('fs')
const axios = require('axios')
const converter = require('json-2-csv')
const data = []
let newData = []
var di = 0
const MAX_CALL = 20
let called = 0

fs.createReadStream('./output/data-all.csv')
    .pipe(csv())
    .on('data', row => data.push(row))
    .on('end', () => {
        newData = data
        
        newData.forEach((row, i) => {
            if (row['lat'] !== 'undefined' || parseInt(row['valid postal']) === 0) return
            if (called < MAX_CALL) {
            // if (row['lat'] === 'undefined') {
                const postal = row['Address'].split(' ').pop()
                axios.get(`https://developers.onemap.sg/commonapi/search?searchVal=${postal}&returnGeom=Y&getAddrDetails=N&pageNum=1`)
                // axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${postal}&key=AIzaSyAvXrCz1aaHL0MH8a6qQFW9zfwS8FP_mks`)
                .then(res => {
                    // if (res.data.results[0]) {
                    row['valid postal'] = res.data.found
                    if (res.data.found === 0) console.log(postal, 'not found')
                    else {
                        const {results} = res.data
                        if (results && results[0]) {
                            const {LATITUDE, LONGTITUDE} = results[0]
                            // const {lat, lng} = res.data.results[0].geometry.location
                            row['lat'] = LATITUDE
                            row['lng'] = LONGTITUDE
                        }
                        // console.log('new row',row)
                    }
                    newData[i] = row
                    di++

                    if (di == MAX_CALL) {
                        converter.json2csv(newData, (err, csvData) => {
                            if (err) throw err
                            fs.writeFile('./output/data-all.csv', csvData, () => {
                                console.log('complete')
                            })
                            
                        })
                    }
                    
                }).catch(err => {
                    console.log('too bad')
                    console.log(err)
                })
                called++
            }
        })
    })
