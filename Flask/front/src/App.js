import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import Chip from "@material-ui/core/Chip";
import Autocomplete from "@material-ui/lab/Autocomplete";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import Rating from "@material-ui/lab/Rating";
import Tooltip from "@material-ui/core/Tooltip";
import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";
import logo from "./logo-salto.png";
import { CircularProgress } from "@material-ui/core";

function App() {
  const [programs, setPrograms] = useState([]);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [suggestions, setSuggestions] = useState(null);
  const [listGenres, setListGenres] = useState(null);
  const [listSsGenres, setListSsGenres] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [selectedSsGenres, setSelectedSsGenres] = useState([]);
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    axios
      .get("http://localhost:5000/programs")
      .then((response) => setPrograms(response.data));
    axios
      .get("http://localhost:5000/genres")
      .then((response) => setListGenres(response.data));
    axios.get("http://localhost:5000/sous-genres").then((response) => {
      const results = response.data;
      setListSsGenres(results.sort());
    });
  }, []);

  useEffect(() => {
    console.log("selectedGenres", selectedGenres);
    if (selectedProgram?.program_id) {
      setLoading(true);
      axios
        .get(`http://localhost:5000/popularity`, {
          params: {
            program_id: selectedProgram.program_id,
            genres: selectedGenres,
            ss_genres: selectedSsGenres,
          },
        })
        .then((response) => {
          setSuggestions(
            response.data.map((suggestion) => ({
              ...suggestion,
              id: suggestion.program_id,
            }))
          );
          setLoading(false);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, [selectedProgram, selectedGenres, selectedSsGenres]);

  const onValueChange = (event, program) => {
    setSuggestions(null);
    if (program?.program_id) {
      setSelectedProgram(program);
      setSelectedGenres([program.tag_genre]);
      setSelectedSsGenres([program.tag_sous_genre_1, ...[program.tag_sous_genre_2 ? program.tag_sous_genre_2 : null] ]);
    } else {
      setSelectedProgram(null);
    }
  };

  const toggleGenre = (genre) => {
    if (selectedGenres.includes(genre)) {
      setSelectedGenres(
        selectedGenres.filter((selectedGenre) => selectedGenre !== genre)
      );
    } else {
      setSelectedGenres([...selectedGenres, genre]);
    }
  };

  const toggleSsGenre = (genre) => {
    if (selectedSsGenres.includes(genre)) {
      setSelectedSsGenres(
        selectedSsGenres.filter((selectedGenre) => selectedGenre !== genre)
      );
    } else {
      setSelectedSsGenres([...selectedSsGenres, genre]);
    }
  };

  return (
    <Container>
      <div>
        <img
          src={logo}
          style={{ width: "200px", margin: "1rem 0px 0rem 1rem" }}
        />
      </div>
      <Autocomplete
        options={programs}
        getOptionLabel={(option) => option.title}
        onChange={onValueChange}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Programme"
            margin="normal"
            variant="outlined"
          />
        )}
      />
      {selectedProgram && (
        <Grid container alignItems="center" style={{ padding: "1rem" }}>
          <Grid item sm={12}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <h3>
                <Chip label={selectedProgram.program_id} />{" "}
                {selectedProgram.title}
                <div style={{ display: loading ? "block" : "none" }}>
                  <CircularProgress />
                </div>
              </h3>
              <ProgramTags program={selectedProgram} />
            </div>
            <div></div>
          </Grid>
          <Grid item sm={6}>
            <div>{selectedProgram.program_description}</div>
            <div>{selectedProgram.description_ready}</div>
          </Grid>
          <Grid item sm={12}>
            <div>
              <h4>Genres</h4>
              {listGenres.map((genre) => (
                <>
                  <Chip
                    key={genre}
                    label={genre}
                    color={
                      selectedGenres.includes(genre) ? "primary" : "default"
                    }
                    onClick={() => toggleGenre(genre)}
                  />{" "}
                </>
              ))}
            </div>
            <div>
              <h4>Sous-Genres</h4>
              {listSsGenres.map((genre) => (
                <>
                  <Chip
                    key={genre}
                    label={genre}
                    color={
                      selectedSsGenres.includes(genre) ? "primary" : "default"
                    }
                    style={{ marginBottom: "0.2rem" }}
                    onClick={() => toggleSsGenre(genre)}
                  />{" "}
                </>
              ))}
            </div>
          </Grid>
        </Grid>
      )}
      {suggestions && suggestions.length !== 0 && (
        <div>
          <h4>Résultats</h4>
          <p>
            Nombre de résultats:{" "}
            <Chip label={suggestions.length} color="secondary" />
          </p>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Id</TableCell>
                  <TableCell>Titre</TableCell>
                  <TableCell>Genre</TableCell>
                  <TableCell>Sous-Genre(s)</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Taux d'engagement</TableCell>
                  <TableCell>Similarité de la description</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {suggestions.slice(0, 20).map((suggestion) => (
                  <TableRow key={suggestion.program_id}>
                    <TableCell>
                      <Chip label={suggestion.program_id} />
                    </TableCell>
                    <TableCell>{suggestion.title}</TableCell>
                    <TableCell>
                      <Chip label={suggestion.tag_genre} color="primary" />
                    </TableCell>
                    <TableCell>
                      {suggestion.tag_sous_genre_1 && (
                        <>
                          <Chip label={suggestion.tag_sous_genre_1} />{" "}
                        </>
                      )}
                      {suggestion.tag_sous_genre_2 && (
                        <Chip label={suggestion.tag_sous_genre_2} />
                      )}
                    </TableCell>
                    <TableCell>{suggestion.program_description}</TableCell>
                    <TableCell>
                      <Tooltip
                        title={((suggestion.ratio_liked / 100) * 5).toFixed(2)}
                      >
                        <div>
                          <Rating
                            value={(suggestion.ratio_liked / 100) * 5}
                            precision={0.1}
                            size="small"
                            readOnly
                          />
                        </div>
                      </Tooltip>
                    </TableCell>
                    <TableCell>
                      {suggestion.cos_similarity.toFixed(6)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )}
      {suggestions && suggestions.length === 0 && loading === false && (
        <div>Aucun résultats</div>
      )}
    </Container>
  );
}

function ProgramTags({ program }) {
  return (
    <div>
      <Chip label={program.tag_genre} color="primary" />{" "}
      {program.tag_sous_genre_1 && (
        <>
          <Chip label={program.tag_sous_genre_1} color="primary" />{" "}
        </>
      )}
      {program.tag_sous_genre_2 && (
        <Chip label={program.tag_sous_genre_2} color="primary" />
      )}
    </div>
  );
}

export default App;
