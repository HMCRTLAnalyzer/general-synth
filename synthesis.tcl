



redirect -file ./results/report.timing         {check_timing}
redirect -file ./results/report.constraints    {report_constraints -all_violators -verbose}
redirect -file ./results/report.paths.max      {report_timing -path end  -delay max -max_paths 200 -nworst 2}
redirect -file ./results/report.full_paths.max {report_timing -path full -delay max -max_paths 5   -nworst 2}
redirect -file ./results/report.paths.min      {report_timing -path end  -delay min -max_paths 200 -nworst 2}
redirect -file ./results/report.full_paths.min {report_timing -path full -delay min -max_paths 5   -nworst 2}
redirect -file ./results/report.refs           {report_reference}
redirect -file ./results/report.area           {report_area}