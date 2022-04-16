CREATE TABLE functions(
    name_id TEXT PRIMARY KEY, 
    name_full TEXT NOT NULL, 
    function_type TEXT NOT NULL,
    symbol TEXT NOT NULL,
    number_input INTEGER DEFAULT 0,
    number_output INTEGER DEFAULT 0,
    pixmap_image TEXT,
    GUI TEXT);

CREATE TABLE imports(
    GUI TEXT,
    import_functions TEXT);

INSERT INTO functions VALUES ( 'EEG', 'EEG Data', 'basis', 'X', 0, 1, NULL, 'import_matlab_eeg');
INSERT INTO functions VALUES ( 'Leadfield','Leadfield Data', 'basis', 'G', 0, 1, NULL, 'gui_load_data');
INSERT INTO functions VALUES ( 'Noise', 'Noise', 'basis', 'N', 0, 2, NULL, 'gui_load_data');
INSERT INTO functions VALUES ( 'Normalized', 'Normalization', 'preprocessing', 'bar', 1, 1, NULL, NULL);

INSERT INTO imports VALUES ('import_matlab_eeg', 'bin.functions_gui.io_gui')