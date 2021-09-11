import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import Box from "@material-ui/core/Box";
import Collapse from "@material-ui/core/Collapse";
import IconButton from "@material-ui/core/IconButton";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Typography from "@material-ui/core/Typography";
import Paper from "@material-ui/core/Paper";
import KeyboardArrowDownIcon from "@material-ui/icons/KeyboardArrowDown";
import KeyboardArrowUpIcon from "@material-ui/icons/KeyboardArrowUp";
import Button from "@material-ui/core/Button";
import GetAppIcon from "@material-ui/icons/GetApp";
import CloudDownloadIcon from "@material-ui/icons/CloudDownload";

const useStyles = makeStyles({
  tableMain: {
    maxHeight: "80vh",
  },
  row: {
    "& > *": {
      borderBottom: "unset",
    },
  },
});

function Row(props) {
  const { row } = props;
  const [open, setOpen] = useState(false);
  const classes = useStyles();

  return (
    <>
      <TableRow className={classes.row}>
        <TableCell>
          <IconButton
            aria-label="expand row"
            size="small"
            onClick={() => setOpen(!open)}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
        <TableCell component="th" scope="row">
          {row.imageName}
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell
          style={{ paddingBottom: 0, paddingTop: 0, maxWidth: "60%" }}
          colSpan={6}
        >
          <Collapse in={open} timeout="auto" unmountOnExit>
            <Box margin={1}>
              <Button
                size="small"
                variant="contained"
                style={{ color: "blue", marginBottom: "20px" }}
                startIcon={<GetAppIcon />}
                href={`/api/v1/download/${row.name}`}
              >
                Download
              </Button>
              <Typography variant="h6" gutterBottom component="div">
                Metadata Record
              </Typography>

              <Table size="small" aria-label="image-metadata">
                <TableHead>
                  <TableRow>
                    <TableCell>Attribute</TableCell>
                    <TableCell>Value</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {Object.entries(row).map((kvPair) => (
                    <TableRow>
                      <TableCell>{kvPair[0]}</TableCell>
                      <TableCell>{kvPair[1]}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
}

export default function CollapsibleTable() {
  const classes = useStyles();
  const [rows, setRows] = useState([]);
  useEffect(async () => {
    const res = await fetch("api/v1/files");
    const data = await res.json();
    if (data) setRows(data);
  }, []);
  return (
    <TableContainer component={Paper} className={classes.tableMain}>
      <Table stickyHeader aria-label="collapsible table">
        <TableHead>
          <TableRow>
            <TableCell>
              <Button
                size="small"
                variant="contained"
                style={{ color: "green" }}
                startIcon={<CloudDownloadIcon />}
                href={`/api/v1/download`}
              >
                Bulk Download
              </Button>
            </TableCell>
            <TableCell>File Name</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((row) => (
            <Row key={row.name} row={row} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
