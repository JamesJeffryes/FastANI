/*
 * A KBase module: FastANI
 */

module FastANI {
    /* fast_ani input */
    typedef structure {
        string workspace_name;
        string query_genome_ref;
        string reference_genome_ref;
    } FastANIParams;

    /* fast_ani output */
    typedef structure {
        string report_name;
        string report_ref;
        float percentage_match;
        int total_fragments;
        int orthologous_matches;
    } FastANIResults;

    funcdef fast_ani(FastANIParams params) returns (FastANIResults results) authentication required;
};