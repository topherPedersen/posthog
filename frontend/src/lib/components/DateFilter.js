import React, { useRef, useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { Row, Col, Modal, Cascader, DatePicker, Button } from 'antd'

import moment from 'moment'

let dateMapping = {
    'Last 24 hours': ['-24h'],
    'Last 48 hours': ['-48h'],
    'Today': ['dStart'],
    'Yesterday': ['-1d', 'dStart'],
    'Last week': ['-7d'],
    'Last 2 weeks': ['-14d'],
    'Last 30 days': ['-30d'],
    'Last 90 days': ['-90d'],
    'Last 180 days': ['-180d'],
    'This month': ['mStart'],
    'Previous month': ['-1mStart', '-1mEnd'],
    'Year to date': ['yStart'],
    'All time': ['all'],
}

let isDate = /([0-9]{4}-[0-9]{2}-[0-9]{2})/

function dateFilterToText(date_from, date_to) {
    if (isDate.test(date_from)) return `${date_from} - ${date_to}`
    if (moment.isMoment(date_from)) return `${date_from.format('YYYY-MM-DD')} - ${date_to.format('YYYY-MM-DD')}`
    let name = 'Last 7 days'
    Object.entries(dateMapping).map(([key, value]) => {
        if (value[0] === date_from && value[1] === date_to) name = key
    })[0]
    return name
}

export function DateFilter({ dateFrom, dateTo, onChange, style }) {
    const [rangeDateFrom, setRangeDateFrom] = useState(isDate.test(dateFrom) && moment(dateFrom).toDate())
    const [rangeDateTo, setRangeDateTo] = useState(isDate.test(dateTo) && moment(dateTo).toDate())
    const [dateRangeOpen, setDateRangeOpen] = useState(false)
    const [open, setOpen] = useState(false)

    function onClickOutside() {
        setOpen(false)
        setDateRangeOpen(false)
    }

    function setDate(fromDate, toDate) {
        onChange(fromDate, toDate)
    }

    function _onChange(v, k) {
        let value = v[v.length - 1]
        if (value === 'Date range') {
            setDateRangeOpen(true)
        } else setDate(dateMapping[value][0], dateMapping[value][1])
    }

    function onBlur() {
        if (dateRangeOpen) return
        onClickOutside()
    }

    function onClick() {
        if (dateRangeOpen) return
        setOpen(!open)
    }

    function dropdownOnClick(e) {
        e.preventDefault()
        setOpen(true)
        setDateRangeOpen(false)
        document.getElementById('daterange_selector').focus()
    }

    function onApplyClick() {
        onClickOutside()
        onChange(moment(rangeDateFrom).format('YYYY-MM-DD'), moment(rangeDateTo).format('YYYY-MM-DD'))
        setDateRangeOpen(false)
    }

    return <>
        {dateRangeOpen && <Modal visible={true} footer={false} onCancel={() => setDateRangeOpen(false)}>
            <DatePickerDropdown
                        onDateFromChange={date => setRangeDateFrom(date)}
                        onDateToChange={date => setRangeDateTo(date)}
                        onApplyClick={onApplyClick}
                        // onClickOutside={onClickOutside}
                        rangeDateFrom={rangeDateFrom}
                        rangeDateTo={rangeDateTo}
                    />
            </Modal>}
        <Cascader
            data-attr="date-filter"
            bordered={false}
            id="daterange_selector"
            // value={dateFilterToText(dateFrom, dateTo)}
            onChange={_onChange}
            style={{
                marginRight: 4,
                ...style,
            }}
            // open={open || dateRangeOpen}
            options={[
                {
                    value: 'Today', label: 'Today'
                },
                {
                    value: 'Yesterday', label: 'Yesterday'
                },
                {
                    value: 'Last...',
                    label: 'Last...',
                    children: [
                        {value: 'Last 24 hours', label: 'Last 24 hours'},
                        {value: 'Last 48 hours', label: 'Last 48 hours'},
                        {value: 'Last week', label: 'Last week'},
                        {value: 'Last 2 weeks', label: 'Last 2 weeks'},
                        {value: 'Last 30 days', label: 'Last 30 days'},
                        {value: 'Last 90 days', label: 'Last 90 days'},
                        {value: 'Last 180 days', label: 'Last 180 days'},
                    ]
                },
                {value: 'This month', label: 'This month'},
                {value: 'Previous month', label: 'Previous month'},
                {value: 'Year to date', label: 'Year to date'},
                {value: 'All time', label: 'All time'},
                {
                    value: 'Date range',
                    'label': 'Date range',
                }
            ]}
            // onBlur={onBlur}
            // onClick={onClick}
            listHeight={400}
            showSearch={{matchInputWidth: true}}
            // dropdownMatchSelectWidth={false}
            // displayRender={label => {
            //     if(label !== 'daterange') return label
            //     return 'hey!'
            //     return (
            //         <DatePickerDropdown
            //             onClick={dropdownOnClick}
            //             onDateFromChange={date => setRangeDateFrom(date)}
            //             onDateToChange={date => setRangeDateTo(date)}
            //             onApplyClick={onApplyClick}
            //             onClickOutside={onClickOutside}
            //             rangeDateFrom={rangeDateFrom}
            //             rangeDateTo={rangeDateTo}
            //         />
            //     )
            // }}
        />
        </>
}

DateFilter.propTypes = {
    onChange: PropTypes.func.isRequired,
}

function DatePickerDropdown(props) {
    const dropdownRef = useRef()
    let [calendarOpen, setCalendarOpen] = useState(false)

    let onClickOutside = event => {
        if (!dropdownRef.current.contains(event.target) && !calendarOpen) {
            props.onClickOutside()
        }
    }

    // useEffect(() => {
    //     document.addEventListener('mousedown', onClickOutside)
    //     return () => {
    //         document.removeEventListener('mousedown', onClickOutside)
    //     }
    // }, [calendarOpen])

    return (
        <div className="dropdown" ref={dropdownRef}>
            <Row>
                <Col span={12}>
                    <label className="secondary">From date</label>
                    <br />
                    <DatePicker
                        popupStyle={{ zIndex: 999999 }}
                        onOpenChange={open => {
                            setCalendarOpen(open)
                        }}
                        autoFocus
                        defaultValue={
                            props.rangeDateFrom
                                ? moment.isMoment(props.rangeDateFrom)
                                    ? props.rangeDateFrom
                                    : moment(props.rangeDateFrom)
                                : null
                        }
                        onChange={props.onDateFromChange}
                    />
                </Col>
                <Col span={12}>
                    <label className="secondary">To date</label>
                    <br />
                    <DatePicker
                        popupStyle={{ zIndex: 999999 }}
                        onOpenChange={open => setCalendarOpen(open)}
                        defaultValue={
                            props.rangeDateTo
                                ? moment.isMoment(props.rangeDateTo)
                                    ? props.rangeDateTo
                                    : moment(props.rangeDateTo)
                                : null
                        }
                        onChange={props.onDateToChange}
                    />
                </Col>
                <Button
                    type="primary"
                    disabled={!props.rangeDateTo || !props.rangeDateFrom}
                    style={{ marginTop: '1rem', marginBottom: '1rem', float: 'right'}}
                    onClick={props.onApplyClick}
                >
                    Apply filter
                </Button>
            </Row>
        </div>
    )
}
